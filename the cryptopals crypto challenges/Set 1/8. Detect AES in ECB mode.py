#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
In this file are a bunch of hex-encoded cipher texts.
One of them has been encrypted with ECB.
Detect it.
Remember that the problem with ECB is that it is stateless and deterministic;
the same 16 byte plaintext block will always produce the same 16 byte cipher text.

# 思路
目的是找出密文, 利用一次密码本原理找出重复的 16 字节串就行了吧
话说这里是对每一行进行统计, 而不是对所有行进行统计, 这也就认为只有一行是用 AES-ECB 进行加密的
"""
from collections import Counter
from itertools import zip_longest

__author__ = '__L1n__w@tch'


def get_repeat_cipher_text(data, times=1, size=1):
    """
    获取重复的密文, 返回统计次数
    :param data: ["line1\n", "line2\n", "line2\n"], 每一行均为十六进制数字
    :param times: 次数, 大于该次数的结果才会返回
    :param size: 要分组的长度
    :return: [("line2", 2), ("line1", 1)]
    """
    output = list()

    for each_line in data:
        # 分组操作
        blocks = divide_group(each_line.strip(), size)
        # 计数操作
        for each in Counter(blocks).most_common():
            # 大于规定次数的才作为返回结果
            if each[1] > times:
                output.append(each)
            else:
                break

    return output


def divide_group(data, size=1):
    """
    对字节流进行分组操作
    :param data: "abcdefghijklmno"
    :param size: 3
    :return: ['abc', 'def', 'ghi', 'jkl', 'mno']
    """
    if len(data) % size != 0:
        raise ValueError

    args = [iter(data)] * size

    blocks = []
    for block in zip_longest(*args):
        blocks.append("".join(block))

    return blocks


if __name__ == "__main__":
    file_name = "challenge8.txt"
    block_size = 16 * 2  # 16 字节, 变成十六进制的话应该是 32 长度

    # 读取文件内容
    # 参数'rU'，可以避免 UNIX 和 Windows 下换行符表示不同的问题 (\r\n, \n)
    with open(file_name, "rU") as f:
        lines = f.readlines()

    repeat_cipher_text = get_repeat_cipher_text(lines, times=2, size=block_size)
    print(repeat_cipher_text)
