#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.20 融合进自己的 pad 以及 unpad 保证 DES 加解密正常
2016.12.19 开始编写信息安全实验要求的工程, 这里是客户端
"""
from basic_class import BasicUI

import socket
import os
import json
import tkinter
import tkinter.messagebox
import tkinter.filedialog
from Crypto.PublicKey import RSA
from Crypto.Cipher import DES

__author__ = '__L1n__w@tch'


class Client(BasicUI):
    sock = None
    client_des_key = None
    contact = "服务端"
    server_rsa_pk = None

    def __init__(self, server_address=(("127.0.0.1", 8083))):
        super().__init__()
        self.server_address = server_address

    def run(self):
        self.root = tkinter.Tk()

        self.sock = self.create_socket()
        self.rsa = self.create_rsa_key()

        self.initialize_root()
        self.initialize_buttons()
        self.initialize_state_label()

        self._update_state_board("初始化成功...\n请点击按钮进行相应操作...")
        self.root.mainloop()

    def create_socket(self):
        socket.setdefaulttimeout(10)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock

    def initialize_root(self):
        # 初始化主窗口大小、标题等
        # self.root.geometry("230x470")
        self.root.title("Mini Filer 客户端 v0.8")
        self.root.resizable(height=False, width=False)

    def initialize_buttons(self):
        # 初始化查看自己公钥按钮
        self._set_show_my_pk_button()

        # 用户头像文件
        self.user_ico = tkinter.PhotoImage(file="user.gif").subsample(2)

        # 初始化客户端相关按钮
        self._set_clients_relevant_buttons()

    def _set_show_my_pk_button(self):
        my_pk_button_frame = tkinter.Frame(self.root)

        my_pk_button = tkinter.Button(my_pk_button_frame,
                                      text="查看自己的公钥", command=self._show_pk)
        my_pk_button.grid()

        my_pk_button_frame.grid(row=0, column=0)

    def _show_pk(self, user="server"):
        sub_window = tkinter.Toplevel()

        if user == "server":
            pk = self.rsa.publickey().exportKey("PEM")
            sub_window.title("自己的公钥")
        else:
            pk = self.server_rsa_pk
            sub_window.title("服务端的公钥")

        text_label = tkinter.Text(sub_window, height=8, width=67)
        text_label.insert(tkinter.END, pk)
        text_label.tag_add("different_tag", "2.38", "5.18")
        text_label.tag_config("different_tag", background="yellow", foreground="red")
        text_label.configure(state=tkinter.DISABLED)
        text_label.grid()

    def _set_clients_relevant_buttons(self):
        def __set_user_ico(frame):
            image_label = tkinter.Label(frame, image=self.user_ico)
            image_label.grid(column=0)

        def __set_function_buttons(frame):
            buttons = dict()

            buttons["connect_button"] = \
                tkinter.Button(frame, text="开始与服务端通信",
                               command=self._connect_client)
            buttons["show_pk_button"] = \
                tkinter.Button(frame, text="查看服务端公钥",
                               command=lambda: self._show_pk(user="Server"), state="disabled")
            buttons["send_file_button"] = \
                tkinter.Button(frame, text="加密文件并发送给服务端",
                               command=self._send_file, state="disabled")
            buttons["decrypt_file_button"] = \
                tkinter.Button(frame, text="解密从服务端接收到的加密文件",
                               command=self._decrypt_file, state="disabled")
            buttons["receive_file_button"] = \
                tkinter.Button(frame, text="接收服务端发送的文件",
                               command=self._receive_file, state="disabled")

            buttons["connect_button"].grid(row=0, sticky=tkinter.E + tkinter.W)
            buttons["show_pk_button"].grid(row=1, sticky=tkinter.E + tkinter.W)
            buttons["send_file_button"].grid(row=2, sticky=tkinter.E + tkinter.W)
            buttons["decrypt_file_button"].grid(row=3, sticky=tkinter.E + tkinter.W)
            buttons["receive_file_button"].grid(row=4, sticky=tkinter.E + tkinter.W)

            return buttons

        clients_frame = tkinter.LabelFrame(self.root)

        # 设置头像
        __set_user_ico(clients_frame)

        # 功能按钮: 新建连接、查看公钥、接收文件、解密其发送的文件、加密文件并发送
        function_frame = tkinter.Frame(clients_frame)
        self.buttons = __set_function_buttons(function_frame)
        function_frame.grid()

        clients_frame.grid()

    def _connect_client(self):
        def __exchange_pk():
            self._update_state_board("开始交换公钥...", new=True)

            my_rsa_pk = self.rsa.publickey().exportKey("PEM")
            self.sock.send(my_rsa_pk)
            self.server_rsa_pk = self.sock.recv(1024)

            self._update_state_board("交换公钥成功!")

        self._update_state_board("尝试与服务端进行连接...", new=True)
        try:
            self.sock.connect(self.server_address)
        except:
            self._update_state_board("连接失败...请确保服务端正常运行...")
            return
        self._update_state_board("成功连接上服务端!")

        __exchange_pk()

        self.buttons["connect_button"].configure(state="disabled")
        self.buttons["show_pk_button"].configure(state="normal")
        self.buttons["send_file_button"].configure(state="normal")
        self.buttons["receive_file_button"].configure(state="normal")

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
            self._update_state_board("发送加密文件中...", new=True)

            encrypted_file = __encrypt_file()
            file_name, file_size = os.path.basename(file_path), len(encrypted_file)
            file_info = json.dumps((file_name, file_size)).ljust(1024)

            sock.send(file_info.encode("utf8"))
            sock.send(encrypted_file)
            sock.recv(len(b"OK"))

            self._update_state_board("发送成功!")

        def __exchange_encrypted_des_key(sock):
            self._update_state_board("开始交换加密的DES密钥...", new=True)

            sock.send(encrypted_des_key[0])
            sock.recv(len("OK"))

            self._update_state_board("交换成功!")

        def __ensure_can_send_file(sock):
            data = sock.recv(len(b"ready to receive file"))
            if b"ready to receive file" == data:
                sock.send(b"ready to send file")
                return
            else:
                raise RuntimeError

        file_path = tkinter.filedialog.askopenfilename(title="要发送的文件为?")
        if file_path == "":
            return
        self._update_state_board("请确保{0}已经准备好开始接收文件...".format(self.contact), new=True)
        try:
            __ensure_can_send_file(self.sock)
        except:
            self._update_state_board("{0}还没准备好开始接收文件...".format(self.contact))
            return

        des_key = __create_des_key(key_size=8)
        encrypted_des_key = __encrypt_des_key(self.server_rsa_pk)
        __exchange_encrypted_des_key(self.sock)
        __send_encrypted_file(self.sock)

        self.buttons["decrypt_file_button"].configure(state="disabled")

    def _decrypt_file(self, encrypted_file=None):
        def __decrypt_des_key(decrypter, encrypted_key):
            plain_text = decrypter.decrypt(encrypted_key)
            return plain_text

        def __decrypt_encrypted_file(file_path):
            des_key = __decrypt_des_key(self.rsa, self.encrypted_des_key)

            with open(file_path, "rb") as f:
                data = f.read()

            counter = slice(0, 8)
            des = DES.new(des_key, DES.MODE_CTR, counter=lambda: data[counter])
            file_contents = des.decrypt(data[8:])

            return self.un_padding(file_contents)

        if encrypted_file is None:
            # http://www.xuebuyuan.com/1918954.html
            encrypted_file = tkinter.filedialog.askopenfilename(title="要解密的文件是?")
            if encrypted_file == "":
                return

        file_path = tkinter.filedialog.asksaveasfilename(title="解密完的文件保存在?")
        file_contents = __decrypt_encrypted_file(encrypted_file)
        self._update_state_board("解密完成!", new=True)
        with open(file_path, "wb") as f:
            f.write(file_contents)

        return file_contents

    def _update_state_board(self, message, new=False):
        if new is True:
            self._update_state_board("*" * 40)
        self.state_board.configure(state="normal")
        self.state_board.insert(tkinter.END, message + "\n")
        self.state_board.configure(state="disabled")
        self.state_board.see(tkinter.END)
        self.root.update()

    def _receive_file(self):
        def __exchange_encrypted_des_key(sock):
            self._update_state_board("开始交换加密的DES密钥...", new=True)

            encrypted_des_key = (sock.recv(1024),)
            sock.send(b"OK")

            self._update_state_board("交换成功!")

            return encrypted_des_key

        def __receive_encrypted_file(client, file_path):
            self._update_state_board("接收加密文件中...", new=True)

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

        def __ask_decrypt_file_now(file_save_path):
            choice = tkinter.messagebox.askyesno(
                message="是否现在解密文件?[PS: 每次发送的文件都会使用新的DES密钥, 故需要在下次发送文件前对接收到的加密文件进行解密]")
            if choice is True:
                self._decrypt_file(file_save_path)

        def __prepare_to_receive_file(sock):
            sock.send(b"ready to receive file")
            data = sock.recv(len(b"ready to send file"))
            if b"ready to send file" == data:
                return
            else:
                raise RuntimeError

        file_save_path = tkinter.filedialog.asksaveasfilename(title="文件保存路径为?")
        if file_save_path == "":
            return
        self._update_state_board("请确保{0}已经准备好开始发送文件...".format(self.contact), new=True)
        try:
            __prepare_to_receive_file(self.sock)
        except:
            self._update_state_board("{0}还没准备好开始发送文件...".format(self.contact))
            return

        self.encrypted_des_key = __exchange_encrypted_des_key(self.sock)
        __receive_encrypted_file(self.sock, file_save_path)
        __ask_decrypt_file_now(file_save_path)

        self.buttons["decrypt_file_button"].configure(state="normal")


def main():
    client = Client()
    client.run()


if __name__ == "__main__":
    main()
