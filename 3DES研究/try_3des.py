#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.11 工作需要, 研究一下 3DES
"""
from Crypto.Cipher import DES3

__author__ = '__L1n__w@tch'


def encrypt(plain_text):
    """
    pass
    :param plain_text: 明文数据
    """
    key = "b" * 24
    des3 = DES3.new(key)
    cipher_text = des3.encrypt(plain_text)
    print(cipher_text)

    return cipher_text


def decrypt(cipher_text):
    """
    解密
    :param key:
    :param cipher_text:
    :return:
    """
    key = "b" * 24
    des3 = DES3.new(key)
    plain_text = des3.decrypt(cipher_text)
    print(plain_text)
    return plain_text


if __name__ == "__main__":
    data = "a" * 8
    cipher_text = encrypt(data)
    plain_text = decrypt(cipher_text)
