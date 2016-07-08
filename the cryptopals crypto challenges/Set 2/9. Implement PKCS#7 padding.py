#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
A block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of plaintext into cipher text.
But we almost never want to transform a single block; we encrypt irregularly-sized messages.
One way we account for irregularly-sized messages is by padding, creating a plaintext that is an even multiple of the
blocksize. The most popular padding scheme is called PKCS#7.
So: pad any block to a specific block length, by appending the number of bytes of padding to the end of the block.
For instance,
    "YELLOW SUBMARINE"
... padded to 20 bytes would be:
    "YELLOW SUBMARINE\x04\x04\x04\x04"
"""

__author__ = '__L1n__w@tch'


def pad(data, length):
    """
    进行填充操作
    :param data: 待填充的数据, b"YELLOW SUBMARINE"
    :param length: 要填充至多长, 20
    :return: 填充后的数据, b"YELLOW SUBMARINE\x04\x04\x04\x04"
    """
    pad_value = length - len(data) % length
    return data + bytes([pad_value]) * pad_value


if __name__ == "__main__":
    no_pad = b"YELLOW SUBMARINE"
    size = 20
    after_pad = b"YELLOW SUBMARINE\x04\x04\x04\x04"
    assert pad(no_pad, size) == after_pad
