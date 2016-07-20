#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
Take your code from the CBC exercise and modify it so that it repurposes the key for CBC encryption as the IV.

Applications sometimes use the key as an IV on the auspices that both the sender and the receiver have to know the key
already, and can save some space by using it as both a key and an IV.

Using the key as an IV is insecure; an attacker that can modify ciphertext in flight can get the receiver to decrypt a
value that will reveal the key.

The CBC code from exercise 16 encrypts a URL string. Verify each byte of the plaintext for ASCII compliance (ie, look
for high-ASCII values). Noncompliant messages should raise an exception or return an error that includes the decrypted plaintext (this happens all the time in real systems, for what it's worth).

Use your code to encrypt a message that is at least 3 blocks long:

AES-CBC(P_1, P_2, P_3) -> C_1, C_2, C_3
Modify the message (you are now the attacker):

C_1, C_2, C_3 -> C_1, 0, C_1
Decrypt the message (you are now the receiver) and raise the appropriate error if high-ASCII is found.

As the attacker, recovering the plaintext from the error, extract the key:

P'_1 XOR P'_3

# 题意
CBC 模式下，如果 IV 和 KEY 使用同一个值, 会导致泄漏 KEY 的漏洞
以下在明文长度为 48 字节的情况下重现该漏洞
方法如下:
    正常加密: AES-CBC(P_1, P_2, P_3) -> C_1, C_2, C_3
    更改: C_1, C_2, C_3 -> C_1, 0, C_1
    获取 Key(存在高 ASCII 码值的情况下): P'_1 XOR P'_3
"""
import os
from Crypto.Cipher import AES

__author__ = '__L1n__w@tch'


class MyCrypto:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, data):
        """
        CBC 加密操作
        :param data: 待加密的明文
        :return: 加密后的结果
        """
        # AES-CBC(P_1, P_2, P_3) -> C_1, C_2, C_3
        return AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(data)

    def decrypt(self, data):
        """
        CBC 解密操作
        :param data: 待解密的密文
        :return: 解密后的结果
        """
        return AES.new(self.key, AES.MODE_CBC, self.iv).decrypt(data)


def attack(crypto, data):
    """
    给定一个 CBC 模式加密的密文, 就可以还原出密钥
    :param crypto: 负责进行 CBC 加解密的对象, 即受攻击的程序
    :param data: 加密得到的密文, C_1, C_2, C_3
    :return: 破解得到的 Key
    """
    # 修改密文, 即C_1, C_2, C_3 -> C_1, 0, C_1
    attack_cipher_text = data[0:16] + bytes(16) + data[0:16]

    result = bytes()
    # 判断是否满足还原密钥的条件(高于 128 的 ASCII 码存在)
    try:
        # appropriate error if high-ASCII is found
        result = crypto.decrypt(attack_cipher_text)
        has_high_ascii(result)
        print("Can not recover the key!")
    except RuntimeError:
        # As the attacker, recovering the plaintext from the error, extract the key:
        # P'_1 XOR P'_3
        key = bytes_xor(result[0:16], result[32:48])
        return key


def has_high_ascii(data):
    """
    判断是否存在高 ASCII 码(ASCII 码值大于等于 128 的), 存在则抛出异常
    :param data:
    :return: None
    """
    for each in data:
        if each >= 128:
            raise RuntimeError("Has high ASCII")


def bytes_xor(bytes_str1, bytes_str2):
    """
    字节流异或
    :param bytes_str1: b"\x00\x01\x02"
    :param bytes_str2: b"\x00\x00\x02"
    :return: b'\x00\x01\x00'
    """
    return bytes([x ^ y for (x, y) in zip(bytes_str1, bytes_str2)])


if __name__ == "__main__":
    aes_key = os.urandom(16)  # 产生一个随机的 KEY
    cbc_iv = aes_key  # 把 KEY 当做 IV 来说用

    # 步骤 1, 正常使用, 得到密文
    plaintext = (b'test' * 12)
    my_crypto = MyCrypto(aes_key, cbc_iv)
    # 进行加密
    cipher_text = my_crypto.encrypt(plaintext)

    # 还原 key
    recovered_key = attack(my_crypto, cipher_text)

    print("Raw AES-KEY: ", aes_key)
    print("Recovered AES-KEY: ", recovered_key)
