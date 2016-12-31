#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.20 融合进自己的 pad 以及 unpad 保证 DES 加解密正常, 已经放进 BaseUI 了
2016.12.19 之前写得有点渣, 重构一下吧
2016.12.19 开始编写信息安全实验要求的工程, 这里是服务端
"""
from basic_class import BasicUI

import socket
import tkinter
import tkinter.messagebox

__author__ = '__L1n__w@tch'


class Server(BasicUI):
    def __init__(self):
        super().__init__()
        self.my_sock = None  # 程序自身的 sock
        self.other_sock = None  # 对方的 sock
        self.other_name = "客户端"
        self.my_name = "服务端"
        self.input_box_message = "监听地址"

    def run(self):
        self.root_tk = tkinter.Tk()

        self.rsa_key = self.create_rsa_key()

        self.initialize_root()
        self.initialize_buttons()
        self.initialize_state_label()
        self.ip_address_box.insert(0, "0.0.0.0:8083".format(self.other_name))

        self._update_state_board("初始化成功...\n请点击按钮进行相应操作...")
        self.root_tk.mainloop()

    def create_socket(self):
        """
        创建 TCP 套接字
        :return:
        """
        # TODO: 需要改用多线程判断超时, 或者新建一个窗口进行处理
        socket.setdefaulttimeout(7)  # 套接字超时时间
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(self.server_address)
        return server_sock

    def _connect_client(self):
        # TODO: 字符串替换, 用变量表示
        def __exchange_pk():
            self._update_state_board("开始交换公钥...", print_sep=True)

            self.other_rsa_pk = self.other_sock.recv(1024)
            my_rsa_pk = self.rsa_key.publickey().exportKey("PEM")
            self.other_sock.send(my_rsa_pk)

            self._update_state_board("交换公钥成功!")

        try:
            self._get_server_address_from_input_box()
            if self.my_sock is None:
                self.my_sock = self.create_socket()
            self._update_state_board("服务端准备就绪...正在监听...", print_sep=True)
            self.my_sock.listen(1)  # 写死了,这里只允许一个客户端连接
            self.other_sock, address = self.my_sock.accept()
        except Exception as e:
            self._update_state_board("没有发现尝试连接的客户端...")
            raise e

        self._update_state_board("成功连接上客户端!")

        __exchange_pk()

        self.buttons["connect_button"].configure(state="disabled")
        self.buttons["show_pk_button"].configure(state="normal")
        self.buttons["send_file_button"].configure(state="normal")
        self.buttons["receive_file_button"].configure(state="normal")

    def sock_connect(self):
        self.other_sock, addr = self.my_sock.accept()
        # tkinter.messagebox.showinfo(title="建立连接", message="正在与客户端进行连接")


def main():
    server = Server()
    server.run()


if __name__ == "__main__":
    main()
