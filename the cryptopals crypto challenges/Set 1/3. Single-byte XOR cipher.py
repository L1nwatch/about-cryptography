#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
The hex encoded string:
    1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
... has been XOR'd against a single character. Find the key, decrypt the message.
You can do this by hand. But don't: write code to do it for you.
How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.
"""
import binascii
import string

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    hex_encoded = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    str_encoded = binascii.unhexlify(hex_encoded)  # 参考网上的, 统一格式后再异或
    for key in string.ascii_letters:
        expand_key = str(key * len(str_encoded)).encode("utf8")  # 统一格式后再异或
        print("Key: {}, Decoded: {}".format(key, bytes([x ^ y for x, y in zip(str_encoded, expand_key)])))
