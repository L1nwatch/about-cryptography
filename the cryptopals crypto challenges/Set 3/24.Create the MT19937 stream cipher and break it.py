# -*- coding: utf-8 -*-
# version: Python3.X
__author__ = '__L1n__w@tch'

# url: http://cryptopals.com/sets/3/challenges/24/
# 题目描述: 我们可以利用MT19937来作为流密码, 用来加密
# 但是这个流密码用来加密某些明文（我们已知后缀的明文）的时候, 我们可以恢复其MT19937所用的seed
# 一个特例是当MT19937流密码用来产生密码令牌时(seed是时间戳), 我们可以恢复其时间戳
# 步骤:
# 1. 实现MT19937作为流密码时的加密
# 2. 当这个流密码用来加密特定类型的明文时, 我们可以重现恢复其seed的漏洞
# 3. 当这个流密码被用来产生密码令牌(seed为时间戳)这一情形时, 我们可以恢复其算法所用的时间戳

import os
import random
import string
import time


class MTStreamCipher:
    def __init__(self, seed):
        self.seed = seed
        self.mt = MT19937(seed)

    def encrypt(self, plaintext):
        # 由于是异或操作, 所以加密也可当作解密函数
        cipher_text = b""

        # 流密码, 按字节异或
        for i in range(len(plaintext)):
            # 由于之前实现的是32bits的MT19937, 所以每隔4个字节就需要重新使用一个新的伪随机数
            if i % 4 == 0:
                cipher = self.mt.extract_number()

            # 依次取出cipher中的1个字节(8bits)
            byte_cipher = (cipher >> (8 * (3 - i % 4))) & 0xff
            # 按字节异或
            cipher_text += bytes([(plaintext[i] ^ byte_cipher)])

        return cipher_text


# class MT19937是chall21的要求, 直接复制过来了(顺带自己美化了一下代码)
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


def test_mtsc_encrypt():
    # 由于流密码使用的是异或操作, 而异或有个性质, 连续异或2次即返回原文
    # 这里利用异或的这个性质来完成加密的验证
    plaintext = b"I am plaintext"
    seed = create_seed()
    # 注意, 这个需要使用同一个种子构造2个mtsc（要不然用到的伪随机值都不一样）
    if MTStreamCipher(seed).encrypt(MTStreamCipher(seed).encrypt(plaintext)) != plaintext:
        print("Encryption Wrong!")
        raise RuntimeError


def create_seed():
    # 题目要求16bit的seed
    # 2个字节即16bit
    return int.from_bytes(os.urandom(2), "big")


def recover_seed():
    plaintext = b""
    seed = create_seed()

    # 添加任意数量的前缀
    for i in range(random.randint(100, 256)):
        plaintext += random.choice(string.printable).encode("ascii")
    # 题目描述说明文后缀带有14个A
    plaintext += b"A" * 14

    cipher_text = MTStreamCipher(seed).encrypt(plaintext)

    # 由于种子seed是2个字节, 所以遍历一遍尝试一下就知道是不是seed了
    print("爆破seed中, 需要时间遍历2^16个数, 请耐心等待", end="")
    for i in range(65536):
        # 只是为了证明程序还在运作
        if i % 1000 == 0:
            print(".", flush=True, end="")

        # 利用异或的性质, 异或2次会导致明文泄漏
        test_decrypt = MTStreamCipher(i).encrypt(cipher_text)
        if test_decrypt[-14:] == b"A" * 14:
            print("爆破成功!")
            print("Raw Seed is ", seed)
            print("Seed is ", i)
            return

    raise Exception("Recover seed fail!")


def test_password_token():
    # generate a random "password reset token"
    mt = MT19937(int(time.time()))

    # 这里产生一个24bytes的随机串
    raw_password_token = create_password_token(mt)

    # 10分钟, 这个爆破思路其实前面做过了, 参考前面的chall22
    crack_time = int(time.time())
    for i in range(600):
        crack_mt = MT19937(crack_time - i)
        crack_password_token = create_password_token(crack_mt)

        if crack_password_token == raw_password_token:
            print("Raw password token: ", raw_password_token)
            print("Recovered password token: ", crack_password_token)
            return

    raise Exception("Crack Password Token Fail!")


def create_password_token(mt):
    password_token = b""
    for i in range(6):
        # 注意这里的mt是4个字节的，所以要6次来产生一个24字节的
        # int.to_bytes()可以将一个整数转为bytes
        password_token += mt.extract_number().to_bytes(4, "big")

    return password_token


def main():
    # 实现流密码加密
    test_mtsc_encrypt()

    # 重现恢复其seed的漏洞
    # 注意, 这里是通过爆破找出其seed的，要遍历65536个数需要一定时间
    recover_seed()

    # 测试一个具体实例, 产生密码令牌的算法中的种子采用时间戳, 目标是恢复时间戳
    test_password_token()


if __name__ == "__main__":
    main()

