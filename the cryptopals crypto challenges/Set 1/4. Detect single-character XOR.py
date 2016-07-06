#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
One of the 60-character strings in this file has been encrypted by single-character XOR.

Find it.

(Your code from #3 should help.)

# 思路
## 思路 1
    词频分析, 比如说找 a 的频率, 但是这里只有一行英文, 所以词频分析法可能不太好
## 思路 2
    通过空格的数量判断是否为英文语句
#
"""
import binascii
import string

__author__ = '__L1n__w@tch'


def is_sentence(bytes_text, space_number=3):
    """
    给一个字节流, 判断是否是英文句子, 判断标准为空格数量
    :param bytes_text: b"I can not say French."
    :param space_number: 空格数量, 比如说 3
    :return: True
    """
    return bytes_text.count(b" ") >= space_number


def bytes_xor(bytes1, bytes2):
    """
    对两个字节流进行异或操作
    :param bytes1: 字节流 1, b"1"
    :param bytes2: 字节流 2, b"2"
    :return: b'\x03'
    """
    return bytes([a ^ b for a, b in zip(bytes1, bytes2)])


def decrypt(encrypt_data):
    """
    尝试每一个可打印字符进行解密操作
    :param encrypt_data: 待解密的字节流, b"\x0e6G\xe8Y-5QJ\x08\x12CX%6\xed=\xe6s@Y\x00\x1e?S\\\xe6'\x102"
    :return: 解密结果, 例如 '0', b'>\x06w\xd8i\x1d\x05az8"sh\x15\x06\xdd\r\xd6Cpi0.\x0fcl\xd6\x17 \x02'
    """
    encrypt_data = binascii.unhexlify(encrypt_data)
    for key in string.printable:
        expand_key = str(key * len(encrypt_data)).encode("utf8")
        yield key, bytes_xor(expand_key, encrypt_data)


if __name__ == '__main__':
    file_name = "challenge4.txt"
    with open(file_name, "r") as f:
        data = f.readlines()

    # 对每一句尝试解密
    for each_line in data:
        # 对每一个尝试解密的结果进行判断
        for key, each_decrypt in decrypt(each_line.strip()):
            if is_sentence(each_decrypt, 5):
                print("Key: {}, Decrypted: {}".format(key, each_decrypt))
