#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
Now that you have ECB and CBC working:
Write a function to generate a random AES key; that's just 16 random bytes.
Write a function that encrypts data under an unknown key --- that is, a function that generates a random key and encrypts under it.
The function should look like:
    encryption_oracle(your-input)
    => [MEANINGLESS JIBBER JABBER]
Under the hood, have the function append 5-10 bytes (count chosen randomly) before the plaintext and 5-10 bytes after the plaintext.
Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC the other half (just use random IVs each time for CBC). Use rand(2) to decide which to use.
Detect the block cipher mode the function is using each time. You should end up with a piece of code that, pointed at a block box that might be encrypting ECB or CBC, tells you which one is happening.

# 题目思路
* 实现加密, 随机选择 ECB 模式或者 CBC 模式进行加密操作
* 给定一段密文, 判断使用 ECB 模式还是使用 CBC 模式

# PS
* 到后面有点卡住，所以参考了下 write_up 的思路写的
* 探测是否为 ECB 模式可以参考 Set1 的 challenge8
"""
import random
import codecs
from Crypto.Cipher import AES
from itertools import zip_longest
from collections import Counter

__author__ = '__L1n__w@tch'


def generate_random_bytes(key_size=16):
    """
    产生指定数量的随机字节
    Write a function to generate a random AES key; that's just 16 random bytes.
    :param key_size: 3
    :return: b'a0D'
    """
    random_bytes = b"".join([bytes([value]) for value in random.sample(range(256), key_size)])
    return random_bytes


def encrypt_oracle(data):
    """
    随机选择 CBC 模式或者 ECB 模式进行加密, 返回加密所使用的模式以及加密后的结果
    :param data: 待加密明文, "plaintext"
    :return: 模式以及加密结果, ("CBC", b"cipher_text")
    """
    size = 16
    key = generate_random_bytes(size)
    encrypt_mode = random.choice([AES.MODE_CBC, AES.MODE_ECB])  # 随机选择一种加密模式
    mode_dict = {AES.MODE_CBC: "CBC", AES.MODE_ECB: "ECB"}

    data = codecs.encode(data, "ascii")  # 将 str 转成 bytes
    # 对数据进行随机化处理
    data = generate_random_bytes(random.randint(5, 10)) + data + generate_random_bytes(random.randint(5, 10))
    data = pad(data, size)  # 填充操作

    if encrypt_mode == AES.MODE_CBC:
        iv = generate_random_bytes(size)
        encrypt_tool = AES.new(key, AES.MODE_CBC, IV=iv)
    elif encrypt_mode == AES.MODE_ECB:
        encrypt_tool = AES.new(key, AES.MODE_ECB)
    else:
        raise RuntimeError("Encrypt_mode is wrong!")

    after_encrypt_data = encrypt_tool.encrypt(data)

    return mode_dict[encrypt_mode], after_encrypt_data


def pad(text, size=16):
    """
    进行填充操作
    :param text: b"abcdefg"
    :param size: 10
    :return: b"abcdefg\x03\x03\x03"
    """
    padding_value = size - len(text) % size
    output = text + bytes([padding_value]) * padding_value
    return output


def is_using_ecb(cipher_text):
    """
    判断是否是使用 ecb 模式, 判断标准: 是否存在两个以上的相同密文(一次密码本特性)
    :param cipher_text: b'a' * 2000
    :return: True
    """
    blocks = divide_group(cipher_text, 16)
    return Counter(blocks).most_common()[0][1] > 1


def divide_group(bytes_data, size):
    """
    对字节流进行分组操作
    :param bytes_data: b"abcdefghi"
    :param size: 3
    :return: [b"abc", b"def", b"ghi"]
    """
    args = [iter(bytes_data)] * size

    blocks = []
    for block in zip_longest(*args):
        blocks.append(b"".join([bytes([value]) for value in block]))

    return blocks


if __name__ == "__main__":
    plaintext = "plaintext" * 160
    (mode, cipher_text) = encrypt_oracle(plaintext)
    print("mode use:{0}, guess mode:{1}".format(mode, "ECB" if is_using_ecb(cipher_text) else "CBC"))
