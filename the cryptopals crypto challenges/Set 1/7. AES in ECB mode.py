#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key
    "YELLOW SUBMARINE".
(case-sensitive, without the quotes; exactly 16 characters;
I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).
Decrypt it. You know the key, after all.
Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.
Do this with code.
You can obviously decrypt this using the OpenSSL command-line tool, but we're having you get ECB working in code for
a reason. You'll need it a lot later on, and not just for attacking ECB.

# 思路
PyCrypto 库自带了 AES, 调用就行了.
关键是密文是啥, 一行解码之后的? 还是某一个 16 字节的解码串?
每一行只有 45 个字符, 不符合 16 的倍数, 那就不是一行一行来了.
干脆全部合起来解密吧... 果然对了
"""
from Crypto.Cipher import AES
import base64

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    key = b"YELLOW SUBMARINE"
    file_name = "challenge7.txt"

    # 读取文件内容
    with open(file_name, "r") as f:
        data = f.readlines()

    # 把所有密文字节流拼接起来
    cipher_text = bytes()
    for each_line in data:
        b64_encoded = each_line.strip()
        b64_decoded = base64.b64decode(b64_encoded)
        cipher_text += b64_decoded

    # 解密操作
    plaintext = AES.new(key, AES.MODE_ECB).decrypt(cipher_text)
    print(plaintext.decode("ascii"))
