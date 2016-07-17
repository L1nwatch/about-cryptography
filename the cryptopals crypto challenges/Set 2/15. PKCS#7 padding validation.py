#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
Write a function that takes a plaintext, determines if it has valid PKCS#7 padding, and strips the padding off.
The string:
    "ICE ICE BABY\x04\x04\x04\x04"
... has valid padding, and produces the result "ICE ICE BABY".
The string:
    "ICE ICE BABY\x05\x05\x05\x05"
... does not have valid padding, nor does:
    "ICE ICE BABY\x01\x02\x03\x04"
If you are writing in a language with exceptions, like Python or Ruby,
make your function throw an exception on bad padding.

Crypto nerds know where we're going with this. Bear with us.
"""

__author__ = '__L1n__w@tch'


def unpad(text, size=16):
    """
    进行解填充操作
    其实这里我有点疑惑，如果原文的最后一个是 \x01 这一类的要认为是合法还是不合法的?
    :param text: b"ICE ICE BABY\x04\x04\x04\x04"
    :param size: 块的长度, 比如 16
    :return: b"ICE ICE BABY"
    """
    # 抛出异常也可以用assert
    assert (len(text) % size == 0)
    padding_value = text[-1]
    # 以下的 -1 注意不要写成 padding_text[-padding_value:-1], 这样导致少了一个字节
    assert (text[-padding_value:] == bytes([padding_value]) * padding_value)
    return text[:len(text) - padding_value]


if __name__ == "__main__":
    texts = [b"ICE ICE BABY\x04\x04\x04\x04", b"ICE ICE BABY\x01\x02\x03\x04", b"ICE ICE BABY\x05\x05\x05\x05"]

    for padding_text in texts:
        print("[*] {pad} 分割线 {pad}".format(pad="=" * 30))
        print("填充字节流: {}, 尝试进行解填充".format(padding_text))
        try:
            unpad_text = unpad(padding_text)
            print("解填充成功, 得到 {}".format(unpad_text))
        except AssertionError:
            print("解填充失败")
