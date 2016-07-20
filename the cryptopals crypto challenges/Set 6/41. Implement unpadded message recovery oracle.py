#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
Nate Lawson says we should stop calling it "RSA padding" and start calling it "RSA armoring". Here's why.

Imagine a web application, again with the Javascript encryption, taking RSA-encrypted messages which (again: Javascript)
 aren't padded before encryption at all.

You can submit an arbitrary RSA blob and the server will return plaintext. But you can't submit the same message twice:
let's say the server keeps hashes of previous messages for some liveness interval, and that the message has an embedded
timestamp:
    {
      time: 1356304276,
      social: '555-55-5555',
    }
You'd like to capture other people's messages and use the server to decrypt them. But when you try, the server takes the
hash of the ciphertext and uses it to reject the request. Any bit you flip in the ciphertext irrevocably scrambles the
decryption.

This turns out to be trivially breakable:

Capture the ciphertext C
Let N and E be the public modulus and exponent respectively
Let S be a random number > 1 mod N. Doesn't matter what.
Now:
C' = ((S**E mod N) C) mod N
Submit C', which appears totally different from C, to the server, recovering P', which appears totally different from P
Now:
          P'
    P = -----  mod N
          S
Oops!

Implement that attack.

Careful about division in cyclic groups.
Remember: you don't simply divide mod N; you multiply by the multiplicative inverse mod N. So you'll need a modinv()
function.

# 题意
跟上一题(Challenge 40)有点联系, 也是加密前没有使用填充导致漏洞的出现

但是这道题多了个限制, 就是不能加密同一个明文两次(上道题是对同一个密文加密了3次)

但同样有漏洞存在, 以下要求我们重现漏洞, 我们不针对明文加密 2 次，而是针对明文的倍数来加密
"""
import gmpy2
import random
from Crypto.Util.number import getPrime

__author__ = '__L1n__w@tch'


def create_rsa_keys(bits_length=1024, e=65537):
    """
    产生有关 RSA 的一切参数, 包括 p, q, n ,phi_n, d, e
    本来想用 pycrypto 库的 RSA 来生成的, 但是这个库至少要求 1024bits, 还是自己手搓吧
    :param bits_length: p 和 q 的位长度限制
    :param e: 指定的 e
    :return: dict(), RSA 的一切参数作为字典返回
    """
    rsa = dict()
    while True:
        p = gmpy2.mpz(getPrime(1024))
        q = gmpy2.mpz(getPrime(1024))
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


def rsa_decrypt(data, n, d):
    """
    实现 RSA 的解密操作
    :param data: 密文, int()
    :param n: 公钥 N, int()
    :param d: 私钥 d, int()
    :return: 解密后的结果
    """
    return gmpy2.powmod(data, d, n)


def rsa_attack(my_rsa, data):
    """
    进行攻击, 参数需要 rsa 中的公钥 N 和 e, 另外还需要 rsa 提供一个解密功能
    :param my_rsa: rsa 相关参数
    :param data: 待破解的密文
    :return: 破解得到的明文
    """
    # Let S be a random number > 1 mod N. Doesn't matter what.
    S = random.randint(2, my_rsa["n"])

    # 攻击原理: C' = ((S**E mod N) C) mod N,
    attack_num = (gmpy2.powmod(S, my_rsa["e"], my_rsa["n"]) * data) % my_rsa["n"]

    # 对 C' 进行解密操作, 这里是模拟 RSA 提供的解密功能
    attack_num = rsa_decrypt(attack_num, my_rsa["n"], my_rsa["d"])

    # P = P' / S mod N
    result = (attack_num * gmpy2.invert(S, my_rsa["n"])) % my_rsa["n"]

    # 这里假设明文字节不超过 1000
    return (int(result).to_bytes(1000, "big")).replace(b"\x00", b"")


if __name__ == "__main__":
    # 创建 RSA
    rsa = create_rsa_keys()
    plaintext = b"I am plaintext"

    # 加密
    cipher_text = rsa_encrypt(plaintext, rsa["n"], rsa["e"])

    # 尝试破耳机得到明文, 需要的参数是公钥以及密文, 需要程序提供一个解密功能
    recovered_plaintext = rsa_attack(rsa, cipher_text)
    print("Raw plaintext: ", plaintext)
    print("Recovered plaintext: ", recovered_plaintext)
    assert (plaintext == recovered_plaintext)
