#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.20 客户端和服务端重复的代码实在太多, 抽象出来一个基类吧
"""
__author__ = '__L1n__w@tch'

from Crypto.PublicKey import RSA
import tkinter


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

    @staticmethod
    def create_rsa_key():
        """
        创建 RSA 密钥, 固定长度 + 固定指数 e
        :return:
        """
        rsa_key = RSA.generate(1024, e=65537)
        return rsa_key

    def initialize_state_label(self):
        """
        初始化状态栏
        :return:
        """
        state_label_frame = tkinter.LabelFrame()

        state_board = tkinter.Text(width=40, height=20)
        state_board.grid()

        state_label_frame.grid()

        self.state_board = state_board

    def _set_clients_relevant_buttons(self, other_name):
        """
        设置界面上的相关按钮
        :param other_name: 通信对方的名字, 比如说自己是服务端, 那么通信方的名字应该就叫客户端
        :return:
        """

        def __set_user_ico(frame):
            image_label = tkinter.Label(frame, image=self.user_ico)
            image_label.grid(column=0)

        def __set_function_buttons(frame):
            buttons = dict()

            buttons["connect_button"] = \
                tkinter.Button(frame, text="开始与客户端通信",
                               command=self._connect_client)
            buttons["show_pk_button"] = \
                tkinter.Button(frame, text="查看客户端公钥",
                               command=lambda: self._show_pk(user="Client"), state="disabled")
            buttons["send_file_button"] = \
                tkinter.Button(frame, text="加密文件并发送给客户端",
                               command=self._send_file, state="disabled")
            buttons["decrypt_file_button"] = \
                tkinter.Button(frame, text="解密从客户端接收到的加密文件",
                               command=self._decrypt_file, state="disabled")
            buttons["receive_file_button"] = \
                tkinter.Button(frame, text="接收客户端发送的文件",
                               command=self._receive_file, state="disabled")

            buttons["connect_button"].grid(row=0, sticky=tkinter.E + tkinter.W)
            buttons["show_pk_button"].grid(row=1, sticky=tkinter.E + tkinter.W)
            buttons["send_file_button"].grid(row=2, sticky=tkinter.E + tkinter.W)
            buttons["decrypt_file_button"].grid(row=3, sticky=tkinter.E + tkinter.W)
            buttons["receive_file_button"].grid(row=4, sticky=tkinter.E + tkinter.W)

            return buttons

        clients_frame = tkinter.LabelFrame(self.root_tk)

        # 设置头像
        __set_user_ico(clients_frame)

        # 功能按钮: 新建连接、查看公钥、接收文件、解密其发送的文件、加密文件并发送
        function_frame = tkinter.Frame(clients_frame)
        self.buttons = __set_function_buttons(function_frame)
        function_frame.grid()

        clients_frame.grid()


if __name__ == "__main__":
    pass
