#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
This is the best-known attack on modern block-cipher cryptography.
Combine your padding code and your CBC code to write two functions.
The first function should select at random one of the following 10 strings:
    MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
    MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
    MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
    MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
    MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
    MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
    MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
    MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
    MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
    MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93
... generate a random AES key (which it should save for all future encryptions), pad the string out to the 16-byte AES
block size and CBC-encrypt it under that key, providing the caller the ciphertext and IV.

The second function should consume the ciphertext produced by the first function, decrypt it, check its padding,
and return true or false depending on whether the padding is valid.

What you're doing here.
This pair of functions approximates AES-CBC encryption as its deployed serverside in web applications;
the second function models the server's consumption of an encrypted session token, as if it was a cookie.

It turns out that it's possible to decrypt the ciphertexts provided by the first function.

The decryption here depends on a side-channel leak by the decryption function.
The leak is the error message that the padding is valid or not.

You can find 100 web pages on how this attack works, so I won't re-explain it. What I'll say is this:

The fundamental insight behind this attack is that the byte 01h is valid padding, and occur in 1/256 trials of
"randomized" plaintexts produced by decrypting a tampered ciphertext.

02h in isolation is not valid padding.

02h 02h is valid padding, but is much less likely to occur randomly than 01h.

03h 03h 03h is even less likely.

So you can assume that if you corrupt a decryption AND it had valid padding, you know what that padding byte is.

It is easy to get tripped up on the fact that CBC plaintexts are "padded".
Padding oracles have nothing to do with the actual padding on a CBC plaintext.
It's an attack that targets a specific bit of code that handles decryption.
You can mount a padding oracle on any CBC block, whether it's padded or not.
# 题意说明
题目要求实现两个函数, 第一个函数选择题目给出的其中一个字符串, 进行加密, 返回(iv | 加密结果)
第二个函数判断一个给定的密文是否合法(通过填充值判断)

这里学答案的，只做第一个分区的破解（利用iv + 第一个分区）
"""
import random
import string
import base64
from Crypto.Cipher import AES

__author__ = '__L1n__w@tch'


def generate_random_bytes(size=16):
    """
    产生一个指定长度的随机字节流
    :param size: 16
    :return: such as b'\x01' * 3 + b"\x09" * 10 + b"\x00" * 3
    """
    return b"".join(random.sample([bytes([value]) for value in range(256)], size))


class MyCrypto:
    def __init__(self, key):
        self.key = key
        self.plaintext = random.choice(self.__get_strings())

    @classmethod
    def __get_strings(cls):
        """
        将题目给的多个字符串放进列表里, 以供选择
        :return: list()
        """
        strings = """MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"""
        return strings.split("\n")

    def get_cipher_text(self):
        """
        返回用来给攻击者破解用的密文
        :return: 密文, 格式为 IV | cipher_text
        """
        return self.encrypt(base64.b64decode(self.plaintext))

    def encrypt(self, data):
        """
        进行加密操作
        :param data: 待加密的明文
        :return: 返回 iv 向量以及加密后的结果, b'16 bit iv' + b'ciphertext'
        """
        iv = generate_random_bytes(16)
        cbc_encrypt = AES.new(self.key, AES.MODE_CBC, iv)
        cipher_text = cbc_encrypt.encrypt(self.pad(data))  # 不需要codecs库
        return iv + cipher_text

    def decrypt(self, data):
        """
        进行解密操作
        :param data: b'16 bit iv' + b'ciphertext'
        :return: b'plaintext'
        """
        iv = data[:16]
        data = data[16:]
        cbc_decrypt = AES.new(self.key, AES.MODE_CBC, iv)
        return cbc_decrypt.decrypt(data)

    def is_valid_cipher_text(self, cipher_text):
        """
        判断所给密文是否合法, 通过解密后判断填充值来确定
        :param cipher_text: b'ciphertext'
        :return: True or False
        """
        result = self.decrypt(cipher_text)
        return self.is_valid_padding(result)

    @classmethod
    def is_valid_padding(cls, data):
        """
        这里可以改进下，利用前面做过的检测是否合法然后抛出异常的函数，我们捕获异常然后返回bool
        :param data:  b'plaintext'
        :return: True or False
        """
        if len(data) % 16 != 0:
            return False

        padding_value = data[-1]
        if data[-padding_value:] != bytes([padding_value]) * padding_value:
            return False

        return True

    @classmethod
    def pad(cls, data, block_size=16):
        """
        进行填充操作
        :param data: b'abc'
        :param block_size: 5
        :return: b'abc\x02\x02'
        """
        padding_value = block_size - len(data) % block_size
        return data + bytes([padding_value]) * padding_value


def attack(judge_function, data):
    """
    攻击者进行攻击, 利用的原理是异或两次相当于没异或
    :param judge_function: 给定一个密文, 该函数会返回密文是否合法
    :param data: 待破解的密文, b'16 bit iv' + b'ciphertext'
    :return: 'plaintext'
    """
    iv = data[:16]
    data = data[16:32]  # 这里只解密第一个分区的明文

    plaintext = str()
    for index in reversed(range(16)):  # range(16, 0, -1) 也可以的
        value = get_valid_padding_cipher_text(plaintext, index, iv)
        attack_cipher_text = bytearray(iv[:index + 1] + value + data)

        # 尝试破解
        for guess in string.printable:
            attack_cipher_text[index] = ord(guess) ^ iv[index] ^ (16 - index)
            if judge_function(bytes(attack_cipher_text)) is True:
                plaintext = guess + plaintext
                break

    return plaintext


def get_valid_padding_cipher_text(plaintext, index, iv):
    """
    返回对应位置异或的中间值
    :param plaintext: "g"
    :param index: 14
    :param iv: b' 16 bit iv'
    :return: b'M'
    """
    output = bytes()

    for i in range(len(plaintext)):
        output = bytes([ord(plaintext[-(i + 1)]) ^ iv[-(i + 1)] ^ (16 - index)]) + output

    return output


if __name__ == "__main__":
    my_crypto = MyCrypto(generate_random_bytes(16))

    # 程序随机选择一个字符串加密后返回
    cipher_text_wait_to_attack = my_crypto.get_cipher_text()

    # 给定一个密文, 判定是否合法, 等下要利用这个函数进行攻击
    my_crypto.is_valid_cipher_text(cipher_text_wait_to_attack)

    # 进行攻击操作
    crack_result = attack(my_crypto.is_valid_cipher_text, cipher_text_wait_to_attack)
    print(crack_result)
