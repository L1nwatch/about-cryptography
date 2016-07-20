#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
When does this ever happen?
This is a bit of a toy problem, but it's very helpful for understanding what RSA is doing (and also for why pure
number-theoretic encryption is terrifying). Trust us, you want to do this before trying the next challenge.
Also, it's fun.

Generate a 1024 bit RSA key pair.
Write an oracle function that uses the private key to answer the question "is the plaintext of this message even or odd"
 (is the last bit of the message 0 or 1). Imagine for instance a server that accepted RSA-encrypted messages and checked
  the parity of their decryption to validate them, and spat out an error if they were of the wrong parity.

Anyways: function returning true or false based on whether the decrypted plaintext was even or odd, and nothing else.

Take the following string and un-Base64 it in your code (without looking at it!) and encrypt it to the public key,
creating a ciphertext:
    VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ==
With your oracle function, you can trivially decrypt the message.

Here's why:
* RSA ciphertexts are just numbers. You can do trivial math on them. You can for instance multiply a ciphertext by the
RSA-encryption of another number; the corresponding plaintext will be the product of those two numbers.
* If you double a ciphertext (multiply it by (2**e)%n), the resulting plaintext will (obviously) be either even or odd.
* If the plaintext after doubling is even, doubling the plaintext didn't wrap the modulus --- the modulus is a prime
number. That means the plaintext is less than half the modulus.

You can repeatedly apply this heuristic, once per bit of the message, checking your oracle function each time.

Your decryption function starts with bounds for the plaintext of [0,n].

Each iteration of the decryption cuts the bounds in half; either the upper bound is reduced by half, or the lower bound is.

After log2(n) iterations, you have the decryption of the message.

Print the upper bound of the message as a string at each iteration; you'll see the message decrypt "hollywood style".

Decrypt the string (after encrypting it to a hidden private key) above.

# 题意
讲述了 RSA（密文是数字）的奇偶性可以被利用会最终导致泄漏其明文

# 步骤：
1. 手搓 RSA(前面的题 41 搓过了我就直接复制了)
2. 写一个判断最后一位奇偶性的函数
3. 加密题目所给的 base64 编码的明文, 最后尝试在不知道明文的情况下破解出来
4. 根据算法所给的描述, 不断测试最后一位来确定明文的范围（明文是数字!）
"""
import gmpy2
import base64
from Crypto.Util.number import getPrime

__author__ = '__L1n__w@tch'


def judge_rsa_parity(cipher_text, n, d):
    """
    判断奇偶性的函数, 这道理我们用到了私钥, 但是现实中某些服务器会告诉你奇偶性结果, 所以原理相同
    :param cipher_text: 待解密的密文
    :param n: 公钥 N
    :param d: 私钥 d
    :return: 奇偶性判断, 奇数返回 True, 偶数返回 False
    """
    plaintext = gmpy2.powmod(cipher_text, d, n)
    # is the last bit of the message 0 or 1?
    return plaintext & 1


# 直接复制自己写的 challenge41 的 code
def create_rsa_keys(bits_length=512, e=65537):
    """
    产生有关 RSA 的一切参数, 包括 p, q, n ,phi_n, d, e
    本来想用 pycrypto 库的 RSA 来生成的, 但是这个库至少要求 1024bits, 还是自己手搓吧
    :param bits_length: p 和 q 的位长度限制
    :param e: 指定的 e
    :return: dict(), RSA 的一切参数作为字典返回
    """
    rsa = dict()
    while True:
        p = gmpy2.mpz(getPrime(bits_length))
        q = gmpy2.mpz(getPrime(bits_length))
        n = p * q
        phi_n = (p - 1) * (q - 1)

        if gmpy2.gcd(e, phi_n) == 1:
            break

    rsa["p"] = p
    rsa["q"] = q
    rsa["n"] = n
    rsa["phi"] = phi_n
    rsa["d"] = gmpy2.invert(e, rsa["phi"])
    rsa["e"] = e

    return rsa


# 直接复制自己写的chall41的code
def rsa_encrypt(data, n, e):
    """
    实现 RSA 的加密操作
    :param data: b"a"
    :param n: 93549667877193339332139489....
    :param e: 65537
    :return: 2870243652248975232299125265865902758928365307196812395....
    """
    data = int.from_bytes(data, "big")
    return gmpy2.powmod(data, e, n)


def crack(data, rsa):
    """
    尝试不断二分逼近得到明文
    :param data: 待破解的密文
    :param rsa: RSA 相关参数
    :return: 破解得到的明文
    """
    raw_cipher_text = data  # 保存原始待破解的密文

    # low和high表示明文范围
    low = 0
    high = rsa["n"] - 1

    while int(low) != int(high):
        # 题目给的算法原理: If you double a ciphertext (multiply it by (2**e)%n)
        # the resulting plaintext will (obviously) be either even or odd.
        data = (2 ** rsa["e"] * data) % rsa["n"]

        if judge_rsa_parity(data, rsa["n"], rsa["d"]):
            # odd: plaintext in upper half of range
            if high - low == 1:
                # 明文一定是整数(不可能是浮点), 这种情况下说明找到了
                low = high
            low += (high - low) // 2  # 地板除法防止产生浮点数
        else:
            # If the plaintext after doubling is even, doubling the plaintext didn't wrap the modulus
            # even: plaintext in the lower half
            if high - low == 1:
                high = low
            high -= (high - low) // 2

        print("明文存在与此范围内: {}, {}".format(low, high))

    # 考虑到可能有误差, 设置个误差范围进行解码
    possible_plaintexts = list()
    for i in range(-10, 10):
        # plaintext = gmpy2.powmod(low + i, rsa["e"], rsa["n"])
        possible_plaintexts.append(int(low + i).to_bytes(1000, "big").replace(b"\x00", b""))

    return possible_plaintexts


if __name__ == "__main__":
    rsa = create_rsa_keys()  # 产生有关 RSA 的一切参数

    # 获得明文
    plaintext = base64.decodebytes(
        b"VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ==")

    # 加密
    cipher_text = rsa_encrypt(plaintext, rsa["n"], rsa["e"])

    # 爆破函数, 类似于二分查找不断缩小范围
    recovered_plaintext = crack(cipher_text, rsa)
    print("Raw plaintext: ", plaintext)
    print("恢复可能有误差, 所以恢复一定范围的值")
    print("Recovered plaintext list: ", recovered_plaintext)
    if plaintext in recovered_plaintext:
        print("恢复成功, 索引值 {} 即为正确的明文".format(recovered_plaintext.index(plaintext)))
