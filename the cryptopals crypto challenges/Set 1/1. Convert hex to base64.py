#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
The string:
49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d
Should produce:
SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
So go ahead and make that happen. You'll need to use this code for the rest of the exercises.

Cryptopals Rule
Always operate on raw bytes, never on encoded strings. Only use hex and base64 for pretty-printing.

# 自己实现 Base64
如果要自己实现的话：
Base64编码要求把3个8位字节（3*8=24）转化为4个6位的字节（4*6=24）
之后在6位的前面补两个0，形成8位一个字节的形式。

base64_map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

# 对所给的16进制转成ascii码后得到
"I'm killing your brain like a poisonous mushroom"
"""
import binascii
import base64
import codecs

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    the_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    answer = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    b64_encoded = base64.b64encode(binascii.unhexlify(the_string))  # 方法一使用 binascii 库
    b64_encoded = base64.b64encode(codecs.decode(the_string, "hex"))  # 方法二使用 codecs 库
    b64_encoded = base64.b64encode(bytes.fromhex(the_string))  # 方法三使用 bytes.fromhex() 函数
    assert answer.encode("utf8") == b64_encoded
