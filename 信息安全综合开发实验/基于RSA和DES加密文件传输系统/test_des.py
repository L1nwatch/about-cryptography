#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.20 DES 要求填充, 所以实现 PKCS#7 填充好了
2016.12.20 尝试 DES 加密
"""
from Crypto.Cipher import DES
import os

__author__ = '__L1n__w@tch'


def padding(data, size=8):
    """
    进行 PKCS#7 填充
    :param data: 待填充的数据, b"YELLOW SUBMARINE"
    :param size: 整数倍数, 比如说 8, 即表示填充到 8 的整数倍
    :return: 填充后的数据, b"YELLOW SUBMARINE\x08\x08\x08\x08\x08\x08\x08\x08"
    """
    pad_value = size - len(data) % size
    return data + bytes([pad_value]) * pad_value


def un_padding(data, size=8):
    """
    进行 PKCS#7 解填充操作
    :param data: b"ICE ICE BABY\x04\x04\x04\x04"
    :param size: 块的长度, 比如 16
    :return: b"ICE ICE BABY"
    """
    # 抛出异常也可以用assert
    assert (len(data) % size == 0)
    padding_value = data[-1]
    # 以下的 -1 注意不要写成 padding_text[-padding_value:-1], 这样导致少了一个字节
    assert (data[-padding_value:] == bytes([padding_value]) * padding_value)
    return data[:len(data) - padding_value]


if __name__ == "__main__":
    key = os.urandom(8)
    counter = os.urandom(8)
    my_des = DES.new(key, DES.MODE_CTR, counter=lambda: counter)

    # DES 是不会自动填充到 8 字节
    cipher_text = my_des.encrypt(padding(b"a"))
    print(cipher_text)

    plain_text = my_des.decrypt(cipher_text)
    print(un_padding(plain_text))
