#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
CBC mode is a block cipher mode that allows us to encrypt irregularly-sized messages, despite the fact that a block cipher natively only transforms individual blocks.
In CBC mode, each cipher text block is added to the next plaintext block before the next call to the cipher core.
The first plaintext block, which has no associated previous cipher text block, is added to a "fake 0th ciphertext block" called the initialization vector, or IV.
Implement CBC mode by hand by taking the ECB function you wrote earlier, making it encrypt instead of decrypt (verify this by decrypting whatever you encrypt to test), and using your XOR function from the previous exercise to combine them.
The file here is intelligible (somewhat) when CBC decrypted against "YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)

Don't cheat.
Do not use OpenSSL's CBC code to do CBC mode, even to verify your results. What's the point of even doing this stuff if you aren't going to learn from it?
# 看题目描述不知道那串 yellow 是干啥的, 看完 writeUp 才知道是 key....
# 每一行读取一下，发现每一行才 61 个字符，所以肯定是整个数据来进行加密解密的
# 自己写的解出来是乱码，然后发现原来文件是 base64 编码的而不是 ascii 的，好吧
"""
from Crypto.Cipher import AES
from itertools import zip_longest
import base64

__author__ = '__L1n__w@tch'


def get_file_content(file):
    """
    按行获取文件内容
    :param file: 待读取文件名,  "challenge10.txt"
    :return: ["line1\n", "line2\n", "line3\n", ...]
    """
    with open(file, "rU") as f:
        lines_list = f.readlines()

    return lines_list


def cbc_decrypt(key, iv, cipher_text):
    """
    CBC 解密操作, 自己手动利用 ECB 模式实现的
    :param key: "YELLOW SUBMARINE"
    :param iv: b'\x00' * 16
    :param cipher_text: b"ciphertext"
    :return: "plaintext"
    """
    block_size = 16
    aes_ecb = AES.new(key, AES.MODE_ECB)  # 题目要求自己用ECB实现CBC吧
    blocks = divide_group(cipher_text, block_size)
    blocks.insert(0, iv)

    result = bytes()
    for index in range(1, len(blocks)):
        tmp = aes_ecb.decrypt(blocks[index])
        result += bytes_xor(tmp, blocks[index - 1])

    return result.decode("utf-8")


def divide_group(data, block_size):
    """
    分组操作
    :param data: b'abcdefghi'
    :param block_size: 3
    :return: [b"abc", b"def", b"ghi"]
    """
    if len(data) % block_size != 0:
        raise ValueError

    args = [iter(data)] * block_size

    blocks = []
    for each_block in zip_longest(*args):
        blocks.append(b"".join([bytes([value]) for value in each_block]))

    return blocks


def bytes_xor(string1, string2):
    """
    字节流异或操作
    :param string1: b'1234567'
    :param string2: b'1234567'
    :return: b'\x00\x00\x00\x00\x00\x00\x00'
    """
    return bytes([a ^ b for a, b in zip(string1, string2)])


if __name__ == "__main__":
    key = "YELLOW SUBMARINE"
    iv = b'\x00' * 16
    file_name = "challenge10.txt"

    lines = get_file_content(file_name)
    cipher_text = b"".join([base64.b64decode(l.strip()) for l in lines])
    plaintext = cbc_decrypt(key, iv, cipher_text)
    print(plaintext)
