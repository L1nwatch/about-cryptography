# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# url: http://cryptopals.com/sets/4/challenges/27/
# 题意: CBC模式下，如果IV和KEY使用同一个值, 会导致泄漏KEY的漏洞
# 以下在明文长度为48字节的情况下重现该漏洞

import os
from Crypto.Cipher import AES


def test(aes_key, iv):
    plaintext = (b'test' * 12)
    aes = AES.new(aes_key, AES.MODE_CBC, iv)

    # AES-CBC(P_1, P_2, P_3) -> C_1, C_2, C_3
    cipher_text = aes.encrypt(plaintext)

    # C_1, C_2, C_3 -> C_1, 0, C_1
    test_cipher_text = cipher_text[0:16] + bytes(16) + cipher_text[0:16]

    try:
        # 注意AES.new()得重新实例化, 不能直接用之前的, 要不然会错, 原因未知
        # appropriate error if high-ASCII is found
        plaintext = AES.new(aes_key, AES.MODE_CBC, iv).decrypt(test_cipher_text)
        has_high_ascii(plaintext)
        print("Can not recover the key!")
    except:
        # As the attacker, recovering the plaintext from the error, extract the key:
        # P'_1 XOR P'_3
        key = xor(plaintext[0:16], plaintext[32:48])
        return key


def has_high_ascii(plaintext):
    for each in plaintext:
        if each >= 128:
            raise RuntimeError


def xor(bytes_str1, bytes_str2):
    """
    这样写不用考虑精度了
    :param hex_str1: b"\x00\x01\x02"
    :param hex_str2: b"\x00\x00\x02"
    :return: b'\x00\x01\x00'
    """
    return bytes([x ^ y for (x, y) in zip(bytes_str1, bytes_str2)])


def main():
    aes_key = os.urandom(16)
    iv = aes_key
    recovered_key = test(aes_key, iv)

    print("Raw AES-KEY: ", aes_key)
    print("Recovered AES-KEY: ", recovered_key)


if __name__ == "__main__":
    main()

