#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
The internal state of MT19937 consists of 624 32 bit integers.

For each batch of 624 outputs, MT permutes that internal state. By permuting state regularly, MT19937 achieves a period
of 2**19937, which is Big.

Each time MT19937 is tapped, an element of its internal state is subjected to a tempering function that diffuses bits
through the result.

The tempering function is invertible; you can write an "untemper" function that takes an MT19937 output and transforms
it back into the corresponding element of the MT19937 state array.

To invert the temper transform, apply the inverse of each of the operations in the temper transform in reverse order.
There are two kinds of operations in the temper transform each applied twice; one is an XOR against a right-shifted value, and the other is an XOR against a left-shifted value AND'd with a magic number. So you'll need code to invert the "right" and the "left" operation.

Once you have "untemper" working, create a new MT19937 generator, tap it for 624 outputs, untemper each of them to
recreate the state of the generator, and splice that state into a new instance of the MT19937 generator.

The new "spliced" generator should predict the values of the original.

Stop and think for a second.
How would you modify MT19937 to make this attack hard? What would happen if you subjected each tempered output to a
cryptographic hash?
# 题意
## 原题背景
MT19937 后输入种子后, 每次调用 extract_number() 后都会输出新的值

如果我们得到由这个生成器产生的其中 624 个值, 我们就有办法得到跟这个 MT19937 同一个种子的随机数生成器

## 要求
实现克隆 MT19937

### 步骤
1. 题目介绍说 MT19937 所使用到的temper是可逆的, 先要求我们写出其逆的算法
2. 利用步骤 1 得到的逆算法, 再利用得到的 624 个值, 我们就能够进行克隆工作
3. 验证是否克隆成功
"""
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


def clone(raw_mt):
    """
    利用得到的逆算法, 再利用 624 个值进行克隆操作
    :param raw_mt: 待克隆的随机数生成器
    :return: 克隆得到的随机数生成器
    """
    clone_mt = MT19937(0)
    for i in range(624):
        clone_mt.MT[i] = reverse_temper(raw_mt.extract_number())

    return clone_mt


def check_clone(raw_mt, clone_mt):
    """
    测试自己是否克隆成功了
    :param raw_mt: 原来的随机数生成器
    :param clone_mt: 克隆得到的随机数生成器
    :return: None
    """
    for i in range(10 ** 4):
        if raw_mt.extract_number() != clone_mt.extract_number():
            raise RuntimeError("Clone Fail!")


def temper(y):
    """
    这是 MT19937 里用到的算法, 参见 MT19937 类的 extract_number()
    :param y:
    :return:
    """
    y ^= y >> 11
    y ^= (y << 7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= y >> 18

    return y


def reverse_temper(y):
    """
    temper 逆算法, 以下算法参考网上资料
        https://jazzy.id.au/2010/09/22/cracking_random_number_generators_part_3.html
    依次进行 RightShiftXor、LeftShiftXorAnd、LeftShiftXorAnd、RightShiftXor
    :param y:
    :return:
    """
    y3 = (y & 0xffffc000)
    y3 |= ((y >> 18) ^ (y & 0x3fff))
    y2 = (y3 & 0x1039ffff)
    y2 |= ((y3 ^ ((y2 << 15) & 0xefc60000)) & 0xfffe0000)
    y1 = y2 & 0x7f
    y1 |= ((((y1 << 7) & 0x9d2c5680) ^ y2) & (0x7f << 7))
    y1 |= ((((y1 << 7) & 0x9d2c5680) ^ y2) & (0x7f << 14))
    y1 |= ((((y1 << 7) & 0x9d2c5680) ^ y2) & (0x7f << 21))
    y1 |= ((((y1 << 7) & 0x9d2c5680) ^ y2) & 0xf0000000)
    y0 = (y1 & 0xffe00000)
    y0 |= (((y0 >> 11) ^ y1) & 0x001ffc00)
    y0 |= (((y0 >> 11) ^ y1) & 0x3ff)

    return y0


def check_reverse_temper_algorithm():
    """
    测试自己写的逆算法是否为正确的
    测试的方法是对一个已知值进行 temper 操作, 如果 reverse_temper 之后值一样, 说明对着
    数据量较小, 可能不能测试边缘数据
    :return:
    """
    for i in range(10 ** 4):
        raw = temper(i)
        recovered = reverse_temper(raw)
        if i != recovered:
            print("Reverse_temper algorithm is Wrong!")
            raise RuntimeError("逆算法有误")


if __name__ == "__main__":
    # 测试自己写的逆算法是否为正确的
    check_reverse_temper_algorithm()

    # 产生一个随机数生成器, 种子是随机值
    raw_mt19937 = MT19937(random.randint(2333, 23333))

    # 克隆工作
    clone_mt19937 = clone(raw_mt19937)

    # 测试克隆是否成功
    check_clone(raw_mt19937, clone_mt19937)

    print("Clone Success!")
