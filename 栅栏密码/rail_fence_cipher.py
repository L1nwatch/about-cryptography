#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 栅栏密码的代码实现
"""
from itertools import zip_longest
import math

__author__ = '__L1n__w@tch'


class RailFence:
    """
    栅栏密码, 初始化需要一个栏数, 内含加密操作与解密操作, 以及内置使用的分组操作
    """

    def __init__(self, number):
        self.num = number  # 规定几个一组

    def encrypt(self, text_decrypted):
        """
        栅栏密码的加密操作
        :param text_decrypted: "WoShiZhongWenBuShiYingWen"
        :return: 栅栏数为 5 时的加密结果, "WZWSnohehgSoniWhnBYeiguin"
        """
        if len(text_decrypted) % self.num != 0:
            raise RuntimeError("待加密的长度需要是栏数的倍数")
        text_encrypted = str()
        groups = RailFence.__divide_group(text_decrypted, self.num)

        for order in range(self.num):
            for each_group in groups:
                text_encrypted += each_group[order]

        return text_encrypted

    def decrypt(self, text_encrypted):
        """
        栅栏密码的解密操作
        :param text_encrypted: "WZWSnohehgSoniWhnBYeiguin"
        :return: 栅栏数为 5 时的解密结果, "WoShiZhongWenBuShiYingWen"
        """
        if len(text_encrypted) % self.num != 0:
            raise RuntimeError("待解密的密文应该是栅栏数的倍数")
        text_decrypted = str()
        groups = RailFence.__divide_group(text_encrypted, len(text_encrypted) // self.num)

        for order in range(len(text_encrypted) // self.num):
            for each_group in groups:
                text_decrypted += each_group[order]

        return text_decrypted

    @staticmethod
    def __divide_group(text, size):
        """
        对字符串进行分组操作
        :param text: "abcdefghi"
        :param size: 3
        :return: ["abc", "def", "ghi"]
        """
        args = [iter(text)] * size
        blocks = list()
        for block in zip_longest(*args):
            blocks.append("".join(block))

        return blocks


class NewRailFence:
    """
    同样是栅栏密码, 但是上面那个要求明文密文长度和栅栏数有联系, 于是新编一个没关联的
    """

    def __init__(self, number):
        self.num = number  # 栅栏数

    def encrypt(self, text_decrypted):
        """
        实现栅栏加密
        :param text_decrypted: str(), 比如 "0123456789"
        :return: str(), 栅栏加密后的结果, 比如栅栏数为 4 的话, 结果为 "0481592637"
        """
        result_str = str()
        groups = self.divide_group(text_decrypted, self.num)
        for i in range(self.num):
            for each_group in groups:
                result_str += each_group.pop(0) if each_group else ""
        return result_str

    def decrypt(self, text_encrypted):
        """
        实现栅栏解密
        :param text_encrypted: str(), 比如 "0481592637"
        :return: str(), 解密后的结果, 比如栅栏数为 4 的话, 解密结果为 "0123456789"
        """
        result_str = str()
        groups = self.average_divide_group(text_encrypted, math.ceil(len(text_encrypted) / self.num))
        for i in range(self.num):
            for each_group in groups:
                result_str += each_group.pop(0) if each_group else ""
        return result_str

    def average_divide_group(self, raw_data, size):
        """
        平均分组
        :param raw_data: str(), 比如 "0481592637"
        :param size: int(), 比如 3
        :return: list(), 比如 ["048", "159", "26", "37"]
        """
        result_list = list()
        raw_group_list = self.divide_group(raw_data, size)

        for i in range(len(raw_group_list) - 1, 1, -1):
            diff = len(raw_group_list[i - 1]) - len(raw_group_list[i])
            if diff != 0 and diff != 1:
                raw_group_list[i].insert(0, raw_group_list[i - 1].pop())
            else:
                break

        return raw_group_list

    def divide_group(self, raw_data, size):
        return [list(each_group) for each_group in list(self.chunks(raw_data, size))]

    @staticmethod
    def chunks(a_list, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(a_list), n):
            yield a_list[i:i + n]


if __name__ == "__main__":
    num = 5
    rail_fence = RailFence(num)
    cipher_text = rail_fence.encrypt("a" * 5 + "b" * 5 + "c" * 5 + "d" * 5 + "e" * 5)
    plaintext = rail_fence.decrypt(cipher_text)
    print("plaintext = {0}\n{num}-cipher_text = {1}".format(plaintext, cipher_text, num=num))

    num = 4
    rf = NewRailFence(num)
    plaintext = "0123456789"
    cipher_text = rf.encrypt(plaintext)
    assert cipher_text == "0481592637", "cipher_text = {}".format(cipher_text)

    plaintext = rf.decrypt(cipher_text)
    assert plaintext == "0123456789", "plaintext = {}".format(plaintext)
