#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.25 重构, 修复已知 BUG
2016.12.20 融合进自己的 pad 以及 unpad 保证 DES 加解密正常, 已经放进 BaseUI 了
2016.12.19 开始编写信息安全实验要求的工程, 这里是客户端
"""
from basic_class import BasicUI

import socket
import tkinter.messagebox

__author__ = '__L1n__w@tch'


class Client(BasicUI):
    def __init__(self):
        super().__init__()
        self.other_sock = None
        self.other_name = "服务端"
        self.my_name = "客户端"
        self.input_box_message = "{}地址".format(self.other_name)

    def run(self):
        self.root_tk = tkinter.Tk()

        self.other_sock = self.create_socket()
        self.rsa_key = self.create_rsa_key()

        self.initialize_root()
        self.initialize_buttons()
        self.initialize_state_label()
        self.ip_address_box.insert(0, "127.0.0.1:8083".format(self.other_name))

        self._update_state_board("初始化成功...\n请点击按钮进行相应操作...")
        self.root_tk.mainloop()

    @staticmethod
    def create_socket():
        #socket.setdefaulttimeout(10)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock

    def _connect_client(self):
        # TODO: 字符串替换, 用变量表示
        def __exchange_pk():
            self._update_state_board("开始交换公钥...", print_sep=True)

            my_rsa_pk = self.rsa_key.publickey().exportKey("PEM")
            self.other_sock.send(my_rsa_pk)
            self.other_rsa_pk = self.other_sock.recv(1024)

            self._update_state_board("交换公钥成功!")

        try:
            self._get_server_address_from_input_box()
            self._update_state_board("尝试与服务端进行连接...", print_sep=True)
            self.other_sock.connect(self.server_address)
            # self.sock_connect(self.server_address)
        except Exception as e:
            self._update_state_board("连接失败...请确保服务端正常运行...")
            raise e
        self._update_state_board("成功连接上服务端!")

        __exchange_pk()

        self.buttons["connect_button"].configure(state="disabled")
        self.buttons["show_pk_button"].configure(state="normal")
        self.buttons["send_file_button"].configure(state="normal")
        self.buttons["receive_file_button"].configure(state="normal")

    def sock_connect(self, address):
        self.other_sock.connect(address)


def main():
    client = Client()
    client.run()


if __name__ == "__main__":
    main()
