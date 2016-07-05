#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
Write a function that takes two equal-length buffers and produces their XOR combination.
If your function works properly, then when you feed it the string:
    1c0111001f010100061a024b53535009181c
... after hex decoding, and when XOR'd against:
    686974207468652062756c6c277320657965
... should produce:
    746865206b696420646f6e277420706c6179

# 题意
实现2个十六进制串的异或
"""
import binascii

__author__ = '__L1n__w@tch'


def hex_xor1(hex_str1, hex_str2):
    """
    十六进制串异或方法 1, int 异或操作符
    :param hex_str1: "1c0111001f010100061a024b53535009181"
    :param hex_str2: "686974207468652062756c6c277320657965"
    :return: "69a96530759875306214cc4892461565e8e4"
    """
    return hex(int(hex_str1, 16) ^ int(hex_str2, 16))[2:]


def hex_xor2(hex_str1, hex_str2):
    """
    十六进制串异或方法 2, 按位异或
    :param hex_str1: "1c0111001f010100061a024b53535009181"
    :param hex_str2: "686974207468652062756c6c277320657965"
    :return: "69a96530759875306214cc4892461565e8e4"
    """
    hex_bytes1 = bytes.fromhex(hex_str1)
    hex_bytes2 = bytes.fromhex(hex_str2)
    xored = bytes([x ^ y for (x, y) in zip(hex_bytes1, hex_bytes2)])
    return binascii.hexlify(xored)


if __name__ == "__main__":
    hex_string1 = "1c0111001f010100061a024b53535009181c"
    hex_string2 = "686974207468652062756c6c277320657965"
    t1 = hex_xor1(hex_string1, hex_string2)
    t2 = hex_xor2(hex_string1, hex_string2)
    assert hex_xor1(hex_string1, hex_string2).encode("utf8") == hex_xor2(hex_string1, hex_string2)
