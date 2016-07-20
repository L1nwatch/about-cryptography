#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
You can create a trivial stream cipher out of any PRNG; use it to generate a sequence of 8 bit outputs and call those
outputs a keystream. XOR each byte of plaintext with each successive byte of keystream.

Write the function that does this for MT19937 using a 16-bit seed. Verify that you can encrypt and decrypt properly.
This code should look similar to your CTR code.

Use your function to encrypt a known plaintext (say, 14 consecutive 'A' characters) prefixed by a random number of
random characters.

From the ciphertext, recover the "key" (the 16 bit seed).

Use the same idea to generate a random "password reset token" using MT19937 seeded from the current time.

Write a function to check if any given password token is actually the product of an MT19937 PRNG seeded with the
current time.

# 题意
我们可以利用 MT19937 来作为流密码, 用来加密
但是这个流密码用来加密某些明文（我们已知后缀的明文）的时候, 我们可以恢复其 MT19937 所用的 seed
一个特例是当 MT19937 流密码用来产生密码令牌时(seed 是时间戳), 我们可以恢复其时间戳

# 步骤:
1. 实现 MT19937 作为流密码时的加密
2. 当这个流密码用来加密特定类型的明文时, 我们可以重现恢复其 seed 的漏洞
3. 当这个流密码被用来产生密码令牌(seed 为时间戳)这一情形时, 我们可以恢复其算法所用的时间戳
"""
import os
import random
import string
import time

__author__ = '__L1n__w@tch'


class MTStreamCipher:
    """
    使用 MT19937 实现流密码
    """

    def __init__(self, seed):
        self.seed = seed
        self.mt = MT19937(seed)

    def encrypt(self, plaintext):
        # 由于是异或操作, 所以加密也可当作解密函数
        cipher_text = bytes()
        number = int()

        # 流密码, 按字节异或
        for i in range(len(plaintext)):
            # 由于之前实现的是32bits的MT19937, 所以每隔4个字节就需要重新使用一个新的伪随机数
            if i % 4 == 0:
                number = self.mt.extract_number()

            # 依次取出cipher中的1个字节(8bits)
            byte_cipher = (number >> (8 * (3 - i % 4))) & 0xff

            # 按字节异或
            cipher_text += bytes([(plaintext[i] ^ byte_cipher)])

        return cipher_text


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


def check_mt_stream_cipher_encrypt():
    """
    检验实现的 MT19937 流密码是否正常
    由于流密码使用的是异或操作, 而异或有个性质, 连续异或 2 次即返回原文, 这里利用异或的这个性质来完成加密的验证
    :return:
    """
    plaintext = b"I am plaintext"
    seed = create_seed()

    # 注意, 这个需要使用同一个种子构造 2 个 mt stream cipher（要不然用到的伪随机值都不一样）
    if MTStreamCipher(seed).encrypt(MTStreamCipher(seed).encrypt(plaintext)) != plaintext:
        raise RuntimeError("Encryption Wrong!")


def create_seed():
    """
    产生一个 16 位, 即两个字节的种子
    :return: 0~2^16 - 1
    """
    return int.from_bytes(os.urandom(2), "big")


def recover_seed(data):
    """
    采取爆破的方式还原种子, 爆破的原理是异或两次会得到明文, 而明文后缀又是已知的
    :param data: 已知明文后缀的密文, 用来爆破种子用的
    :return: int(), 0 ~ 2 ** 16 - 1 的一个数
    """
    # 由于种子seed是2个字节, 所以遍历一遍尝试一下就知道是不是seed了
    print("爆破 seed 中, 需要时间遍历 2^16 个数, 请耐心等待", end="")
    for i in range(2 ** 16):
        # 只是为了证明程序还在运作
        if i % 1000 == 0:
            print(".", flush=True, end="")

        # 利用异或的性质, 异或2次会导致明文泄漏
        test_decrypt = MTStreamCipher(i).encrypt(data)
        if test_decrypt[-14:] == b"A" * 14:  # 根据明文后缀进行判断
            return i

    raise RuntimeError("Recover seed fail!")


def try_to_crack_password_token():
    """
    测试一个具体实例, 产生密码令牌的算法中的种子采用时间戳, 目标是恢复时间戳
    :return:
    """
    # 以时间戳为种子产生一个随机数生成器, generate a random "password reset token"
    mt = MT19937(int(time.time()))

    # 这里产生一个 24bytes 的随机串
    raw_password_token = create_password_token(mt)

    # 10 分钟, 这个爆破思路其实前面做过了, 参考前面的 challenge22
    crack_time = int(time.time())
    for i in range(600):
        crack_mt = MT19937(crack_time - i)
        crack_password_token = create_password_token(crack_mt)

        if crack_password_token == raw_password_token:
            print("Raw password token: ", raw_password_token)
            print("Recovered password token: ", crack_password_token)
            return

    raise RuntimeError("Crack Password Token Fail!")


def create_password_token(mt):
    """
    产生 24 字节的随机字节流
    :param mt: 随机数生成器
    :return: 24 字节的随机字节流
    """
    password_token = bytes()
    for i in range(6):
        # 注意这里的 mt 是 4 个字节的，所以要 6 次来产生一个 24 字节的
        # int.to_bytes()可以将一个整数转为bytes
        password_token += mt.extract_number().to_bytes(4, "big")

    return password_token


if __name__ == "__main__":
    # 验证流密码加密
    check_mt_stream_cipher_encrypt()

    # 实现流密码加密
    plaintext = bytes()
    seed = create_seed()  # 产生一个种子

    # 添加任意数量的前缀
    for i in range(random.randint(100, 256)):
        plaintext += random.choice(string.printable).encode("ascii")
    # 根据题目描述, 明文后缀带有 14 个A(即已知明文后缀)
    plaintext += b"A" * 14
    cipher_text = MTStreamCipher(seed).encrypt(plaintext)

    # 重现恢复其 seed 的漏洞
    # 注意, 这里是通过爆破找出其 seed 的，要遍历 65536 个数需要一定时间
    crack_seed = recover_seed(cipher_text)
    print("爆破成功!")
    print("Raw Seed is ", seed)
    print("Seed is ", crack_seed)

    # 演示一个具体实例, 产生密码令牌的算法中的种子采用时间戳, 目标是恢复时间戳
    try_to_crack_password_token()
