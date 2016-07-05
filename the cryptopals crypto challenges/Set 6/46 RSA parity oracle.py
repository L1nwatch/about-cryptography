# -*- coding: utf-8 -*-
# version: Python3.X
__author__ = '__L1n__w@tch'

# url: http://cryptopals.com/sets/6/challenges/46/
# 题意: 讲述了RSA（密文是数字）的奇偶性可以被利用会最终导致泄漏其明文
# 步骤：
# 1. 手搓RSA(前面的题41搓过了我就直接复制了)
# 2. 写一个判断最后一位奇偶性的函数
# 3. 加密题目所给的base64编码的明文, 最后尝试在不知道明文的情况下破解出来
# 4. 利用算法所给的描述, 不断测试最后一位来确定明文的范围（明文是数字!）

import gmpy2
import base64
from Crypto.Util.number import getPrime

# 判断奇偶性的函数, 这道理我们用到了私钥, 但是现实中某些服务器会告诉你奇偶性结果, 所以原理相同
def judge_rsa_parity(cipher_text, n, d):
    plaintext = gmpy2.powmod(cipher_text, d, n)
    # is the last bit of the message 0 or 1?
    return plaintext & 1


# 直接复制自己写的chall41的code
def create_rsa_keys(bits_length=512, e=65537):
    # 本来想用pycrypto库的RSA来生成的, 但是这个库至少要求1024bits, 还是自己手搓吧
    rsa = dict()
    while True:
        p = getPrime(bits_length)
        q = getPrime(bits_length)

        if gmpy2.gcd(p, e) == 1 and gmpy2.gcd(q, e) == 1:
            break

    rsa["p"] = p
    rsa["q"] = q
    rsa["n"] = p * q
    rsa["phi"] = (p - 1) * (q - 1)
    rsa["d"] = gmpy2.invert(e, rsa["phi"])
    rsa["e"] = e

    return rsa


# 直接复制自己写的chall41的code
def rsa_encrypt(plaintext, n, e):
    """
    :param plaintext: b"a"
    :param n: 93549667877193339332139489....
    :param e: 65537
    :return: 2870243652248975232299125265865902758928365307196812395....
    """
    plaintext = int.from_bytes(plaintext, "big")
    return gmpy2.powmod(plaintext, e, n)


def main():
    rsa = create_rsa_keys()
    plaintext = base64.decodebytes(
        b"VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ==")
    cipher_text = rsa_encrypt(plaintext, rsa["n"], rsa["e"])

    # 爆破函数, 类似于二分查找不断缩小范围
    recovered_plaintext = crack(cipher_text, rsa)
    print("Raw plaintext: ", plaintext)
    print("恢复可能有误差, 所以恢复一定范围的值")
    print("Recovered plaintext: ", recovered_plaintext)
    if plaintext in recovered_plaintext:
        print("恢复成功, 序号: ", recovered_plaintext.index(plaintext))


def crack(cipher_text, rsa):
    raw_cipher_text = cipher_text
    # low和high表示明文范围
    low = 0
    high = rsa["n"] - 1

    while int(low) != int(high):
        # 题目给的算法原理: If you double a ciphertext (multiply it by (2**e)%n)
        # the resulting plaintext will (obviously) be either even or odd.
        cipher_text = (2 ** rsa["e"] * cipher_text) % rsa["n"]

        if judge_rsa_parity(cipher_text, rsa["n"], rsa["d"]):
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

    # 考虑到可能有误差, 设置个误差范围进行解码
    possible_plaintexts = list()
    for i in range(-10, 10):
        plaintext = gmpy2.powmod(low + i, rsa["e"], rsa["n"])
        possible_plaintexts.append(int(low + i).to_bytes(1000, "big").replace(b"\x00", b""))

    return possible_plaintexts


if __name__ == "__main__":
    main()

