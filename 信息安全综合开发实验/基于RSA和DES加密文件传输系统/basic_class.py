#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.20 客户端和服务端重复的代码实在太多, 抽象出来一个基类吧
"""
__author__ = '__L1n__w@tch'


class BasicUI:
    def __init__(self):
        self.root_tk = None  # 主窗体
        self.state_board = None  # 状态栏

    @staticmethod
    def padding(data, size=8):
        """
        进行 PKCS#7 填充
        :param data: 待填充的数据, b"YELLOW SUBMARINE"
        :param size: 整数倍数, 比如说 8, 即表示填充到 8 的整数倍
        :return: 填充后的数据, b"YELLOW SUBMARINE\x08\x08\x08\x08\x08\x08\x08\x08"
        """
        pad_value = size - len(data) % size
        return data + bytes([pad_value]) * pad_value

    @staticmethod
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
    pass
