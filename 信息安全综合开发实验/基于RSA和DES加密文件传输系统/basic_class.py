#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.25 重构得差不多了
2016.12.20 客户端和服务端重复的代码实在太多, 抽象出来一个基类吧
"""

import os
import json
import socket
import tkinter
import tkinter.messagebox
import tkinter.filedialog
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES

__author__ = '__L1n__w@tch'


class BasicUI:
    def __init__(self):
        self.root_tk = None  # 主窗体
        self.state_board = None  # 状态栏\
        self.other_sock = None  # 交互用的 sock
        self.other_name = None  # 对方的名字
        self.my_name = None  # 自己的名字
        self.other_rsa_pk = None  # 对方的公钥
        self.rsa_key = None  # 自己的公钥
        self.user_ico = None  # 头像文件

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
        # TODO: 解密不合法文件时处理
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

        def __set_function_buttons(frame, name):
            buttons = dict()

            buttons["connect_button"] = \
                tkinter.Button(frame, text="开始与{}通信".format(name),
                               command=self._connect_client)
            buttons["show_pk_button"] = \
                tkinter.Button(frame, text="查看{}公钥".format(name),
                               command=lambda: self._show_pk(False, name), state="disabled")
            buttons["send_file_button"] = \
                tkinter.Button(frame, text="加密文件并发送给{}".format(name),
                               command=self._send_file, state="disabled")
            buttons["decrypt_file_button"] = \
                tkinter.Button(frame, text="解密从{}接收到的加密文件".format(name),
                               command=self._decrypt_file, state="disabled")
            buttons["receive_file_button"] = \
                tkinter.Button(frame, text="接收{}发送的文件".format(name),
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
        self.buttons = __set_function_buttons(function_frame, other_name)
        function_frame.grid()

        clients_frame.grid()

    def _set_show_my_pk_button(self):
        """
        设置显示自己公钥的按钮
        :return:
        """
        my_pk_button_frame = tkinter.Frame(self.root_tk)

        my_pk_button = tkinter.Button(my_pk_button_frame,
                                      text="查看自己的公钥", command=self._show_pk)
        my_pk_button.grid()

        my_pk_button_frame.grid(row=0, column=0)

    def _show_pk(self, show_my_pubkey=True, other_name="对方"):
        """
        显示公钥窗口的内部细节实现
        :param show_my_pubkey: 是否显示自己的公钥
        :param other_name: 如果不是显示自己的公钥, 则是显示(other_name)的公钥?
        :return:
        """
        sub_window = tkinter.Toplevel()

        if show_my_pubkey:
            pk = self.rsa_key.publickey().exportKey("PEM")
            sub_window.title("自己的公钥")
        else:
            pk = self.other_rsa_pk
            sub_window.title("{}的公钥".format(other_name))

        text_label = tkinter.Text(sub_window, height=8, width=67)
        text_label.insert(tkinter.END, pk)
        text_label.tag_add("different_tag", "2.38", "5.18")
        text_label.tag_config("different_tag", background="yellow", foreground="red")
        text_label.configure(state=tkinter.DISABLED)
        text_label.grid()
        sub_window.grid()

    def _receive_file(self):
        """
        实现接收文件的流程
        :return:
        """

        def __exchange_encrypted_des_key(sock):
            self._update_state_board("开始交换加密的DES密钥...", print_sep=True)

            encrypted_des_key = (sock.recv(1024),)
            sock.send(b"OK")

            self._update_state_board("交换成功!")

            return encrypted_des_key

        def __receive_encrypted_file(client, file_path):
            self._update_state_board("接收加密文件中...", print_sep=True)

            file_name, file_size = json.loads(client.recv(1024).decode("utf8").strip())
            with open(file_path, "wb") as f:
                while True:
                    data = client.recv(1024)
                    f.write(data)

                    file_size -= len(data)
                    if file_size <= 0:
                        break
            client.send("OK".encode("utf8"))

            self._update_state_board("接收成功!")

        def __ask_decrypt_file_now(path):
            choice = tkinter.messagebox.askyesno(
                message="是否现在解密文件?[PS: 每次发送的文件都会使用新的DES密钥, 故需要在下次发送文件前对接收到的加密文件进行解密]")
            if choice is True:
                self._decrypt_file(path)

        def __prepare_to_receive_file(sock):
            sock.send(b"ready to receive file")
            data = sock.recv(len(b"ready to send file"))
            if b"ready to send file" == data:
                return
            else:
                print(data)
                raise socket.timeout

        file_save_path = tkinter.filedialog.asksaveasfilename(title="文件保存路径为?")
        if file_save_path == "":
            return False
        self._update_state_board("请确保{0}已经准备好开始发送文件...".format(self.other_name), print_sep=True)
        try:
            __prepare_to_receive_file(self.other_sock)
        except socket.timeout:
            self._update_state_board("{0}还没准备好开始发送文件...".format(self.other_name))
            return False

        self.encrypted_des_key = __exchange_encrypted_des_key(self.other_sock)
        __receive_encrypted_file(self.other_sock, file_save_path)
        __ask_decrypt_file_now(file_save_path)

        self.buttons["decrypt_file_button"].configure(state="normal")

    def _update_state_board(self, message, print_sep=False):
        """
        更新状态栏
        :param message: 传给状态栏的信息
        :param print_sep: 是否要打印分隔符
        :return:
        """
        if print_sep is True:
            self._update_state_board("*" * 40)
        self.state_board.configure(state="normal")
        self.state_board.insert(tkinter.END, message + "\n")
        self.state_board.configure(state="disabled")
        self.state_board.see(tkinter.END)
        self.state_board.update()
        # self.root_tk.update()

    def initialize_buttons(self):
        # 初始化查看自己公钥按钮
        self._set_show_my_pk_button()

        # 用户头像文件
        self.user_ico = tkinter.PhotoImage(file="user.gif").subsample(2)

        # 初始化相关按钮
        self._set_clients_relevant_buttons(self.other_name)

    def initialize_root(self):
        # 初始化主窗口大小、标题等
        # self.root.geometry("230x470")
        self.root_tk.title("Mini Filer {} v0.8".format(self.my_name))
        self.root_tk.resizable(height=False, width=False)

    def _decrypt_file(self, encrypted_file=None):
        def __decrypt_des_key(decrypter, encrypted_key):
            plain_text = decrypter.decrypt(encrypted_key)
            return plain_text

        def __decrypt_encrypted_file(path):
            des_key = __decrypt_des_key(self.rsa_key, self.encrypted_des_key)

            with open(path, "rb") as file:
                data = file.read()

            counter = slice(0, 8)
            des = DES.new(des_key, DES.MODE_CTR, counter=lambda: data[counter])
            decrypt_content = des.decrypt(data[8:])

            return self.un_padding(decrypt_content)

        if encrypted_file is None:
            # http://www.xuebuyuan.com/1918954.html
            encrypted_file = tkinter.filedialog.askopenfilename(title="要解密的文件是?")
            if encrypted_file == "":
                return

        file_path = tkinter.filedialog.asksaveasfilename(title="解密完的文件保存在?")
        file_contents = __decrypt_encrypted_file(encrypted_file)
        self._update_state_board("解密完成!", print_sep=True)
        with open(file_path, "wb") as f:
            f.write(file_contents)

        return file_contents

    def _send_file(self):
        def __encrypt_file():
            # CTR模式使用: http://stackoverflow.com/questions/3154998/pycrypto-problem-using-desctr
            counter = os.urandom(8)
            encrypt_sir = DES.new(des_key, DES.MODE_CTR, counter=lambda: counter)

            with open(file_path, "rb") as f:
                cipher_text = encrypt_sir.encrypt(self.padding(f.read()))

            return counter + cipher_text

        def __encrypt_des_key(rsa_pk):
            rsa = RSA.importKey(rsa_pk)
            cipher_text = rsa.encrypt(des_key, rsa_pk)
            return cipher_text

        def __create_des_key(key_size):
            return os.urandom(key_size)

        def __send_encrypted_file(sock):
            self._update_state_board("发送加密文件中...", print_sep=True)

            encrypted_file = __encrypt_file()
            file_name, file_size = os.path.basename(file_path), len(encrypted_file)
            file_info = json.dumps((file_name, file_size)).ljust(1024)

            sock.send(file_info.encode("utf8"))
            sock.send(encrypted_file)
            sock.recv(len(b"OK"))

            self._update_state_board("发送成功!")

        def __exchange_encrypted_des_key(sock):
            self._update_state_board("开始交换加密的DES密钥...", print_sep=True)

            sock.send(encrypted_des_key[0])
            sock.recv(len(b"OK"))

            self._update_state_board("交换成功!")

        def __ensure_can_send_file(sock):
            data = sock.recv(len(b"ready to receive file"))
            if b"ready to receive file" == data:
                sock.send(b"ready to send file")
                return False
            else:
                raise socket.timeout

        file_path = tkinter.filedialog.askopenfilename(title="要发送的文件为?")
        if file_path == "":
            return False

        self._update_state_board("请确保{0}已经准备好开始接收文件...".format(self.other_name), print_sep=True)
        try:
            __ensure_can_send_file(self.other_sock)
        except socket.timeout:
            self._update_state_board("{0}还没准备好开始接收文件...".format(self.other_name))
            return False

        des_key = __create_des_key(key_size=8)
        encrypted_des_key = __encrypt_des_key(self.other_rsa_pk)
        __exchange_encrypted_des_key(self.other_sock)
        __send_encrypted_file(self.other_sock)

        self.buttons["decrypt_file_button"].configure(state="disabled")


if __name__ == "__main__":
    pass
