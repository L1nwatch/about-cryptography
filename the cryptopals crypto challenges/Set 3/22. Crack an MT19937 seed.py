#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
Make sure your MT19937 accepts an integer seed value. Test it (verify that you're getting the same sequence of outputs
given a seed).

Write a routine that performs the following operation:

Wait a random number of seconds between, I don't know, 40 and 1000.
Seeds the RNG with the current Unix timestamp
Waits a random number of seconds again.
Returns the first 32 bit output of the RNG.
You get the idea. Go get coffee while it runs. Or just simulate the passage of time, although you're missing some of
the fun of this exercise if you do that.

From the 32 bit RNG output, discover the seed.
# 题意
MT19937 的种子是可以被破解出来的, 题目要求重现该漏洞

## 步骤：
1. 题目要求验证 MT19937 对同一个种子会产生相同的值
2. 按照题目给的 4 个步骤编写子程序, 重现漏洞
"""
import time
import random

__author__ = '__L1n__w@tch'


# class MT19937 是 challenge21 的要求, 直接复制过来了(顺带自己美化了一下代码)
class MT19937:
    def __init__(self, seed):
        self.MT = [0] * 624
        self.index = 0
        self.seed = 0
        self.initialize_generator(seed)

    def initialize_generator(self, seed):
        self.MT[0] = seed
        for i in range(1, 624):
            self.MT[i] = 0xffffffff & (0x6c078965 * (self.MT[i - 1] ^ (self.MT[i - 1] >> 30)) + i)

    def extract_number(self):
        if self.index == 0:
            self.generate_numbers()

        y = self.MT[self.index]
        y ^= (y >> 11)
        y ^= ((y << 7) & 0x9d2c5680)
        y ^= ((y << 15) & 0xefc60000)
        y ^= (y >> 18)

        self.index = (self.index + 1) % 624
        return y

    def generate_numbers(self):
        for i in range(624):
            y = (self.MT[i] & 0x80000000) + (self.MT[(i + 1) % 624] & 0x7fffffff)
            self.MT[i] = self.MT[(i + 397) % 624] ^ (y >> 1)
            if (y % 2) != 0:
                self.MT[i] ^= 0x9908b0df


def try_crack():
    """
    尝试进行爆破, 按照题目给的 4 步来依次编写程序
    :return:
    """
    # Wait a random number of seconds between, I don't know, 40 and 1000.
    # 要我们手动等40s，可以用 time.sleep(40), 不过这里通过插入已经延后了时间的种子来实现
    wait_time = random.randint(40, 1000)

    # Seeds the RNG with the current Unix timestamp
    raw_seed = int(time.time()) + wait_time
    mt = MT19937(raw_seed).extract_number()

    # Waits a random number of seconds again.
    # 手动等time.sleep(40). 看crack_seed()函数，内置的random.randint(2000,3000)就模拟等了2000s
    wait_time = random.randint(40, 1000)

    # Returns the first 32 bit output of the RNG.
    recovered_seed = crack_seed(mt)
    print("Raw Seed = {0}\nRecovered Seed = {1}".format(raw_seed, recovered_seed))


def crack_seed(wait_to_crack_time):
    # 由于只是等待了 2 个 wait_time，即顶多等了 2000s 左右, 自己手动遍历一遍就可以猜出 raw_seed 了
    crack_time = int(time.time()) + random.randint(2000, 3000)
    for wait_time in range(10000):
        test_seed = crack_time - wait_time
        mt = MT19937(test_seed).extract_number()

        if mt == wait_to_crack_time:
            return test_seed


def verify_mt19937():
    """
    验证 MT19937 是不是给定一个种子之后以后产生的所有数值都相等
    :return:
    """
    mt1 = MT19937(6666)
    mt2 = MT19937(6666)
    for i in range(10 ** 4):
        # 若不相等会抛出异常
        assert (mt1.extract_number() == mt2.extract_number())


if __name__ == "__main__":
    try:
        verify_mt19937()
    except AssertionError:
        print("MT19937编写有误, 对同一个种子产生了不同的值")

    try_crack()
