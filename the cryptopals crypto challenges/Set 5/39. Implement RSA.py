#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
There are two annoying things about implementing RSA. Both of them involve key generation; the actual encryption/decryption in RSA is trivial.
First, you need to generate random primes. You can't just agree on a prime ahead of time, like you do in DH.
You can write this algorithm yourself, but I just cheat and use OpenSSL's BN library to do the work.
The second is that you need an "invmod" operation (the multiplicative inverse), which is not an operation that is wired
into your language. The algorithm is just a couple lines, but I always lose an hour getting it to work.
I recommend you not bother with primegen, but do take the time to get your own EGCD and invmod algorithm working.
Now:
    Generate 2 random primes. We'll use small numbers to start, so you can just pick them out of a prime table.
    Call them "p" and "q".
    Let n be p * q. Your RSA math is modulo n.
    Let et be (p-1)*(q-1) (the "totient"). You need this value only for keygen.
    Let e be 3.
    Compute d = invmod(e, et). invmod(17, 3120) is 2753.
    Your public key is [e, n]. Your private key is [d, n].
    To encrypt: c = m**e%n. To decrypt: m = c**d%n
    Test this out with a number, like "42".
    Repeat with bignum primes (keep e=3).
Finally, to encrypt a string, do something cheesy, like convert the string to hex and put "0x" on the front of it to
turn it into a number. The math cares not how stupidly you feed it strings.

# 题意: 手动实现RSA, 包括加密和解密等操作
## 步骤:
    1. 产生 2 个随机质数, p,q
    2. n = p * q
    3. et = (p - 1) * (q - 1)
    4. 1 < e < phi(p, q)
    5. d = invmod(e, et)(exp, invmod(17,3120) = 2753)
    6. PK = [E, N], SK = [D, N]
    7. Encrypt: c = m ** e % n, Decrypt: m = c ** d % n
    8. 对代码进行测试（测试加密, 解密等）
    9. 十六进制表示
"""
import gmpy2
import binascii
from Crypto.Util.number import getPrime

__author__ = '__L1n__w@tch'


class MyRSA:
    def __init__(self, p=None, q=None, bit_length=512, e=None):
        """
        设定 p 和 q, 如果没有则根据 bit_length 来产生对应长度的素数
        :param p: 素数 p
        :param q: 素数 q
        :param bit_length: 比特位的长度
        """
        if p and q and gmpy2.is_prime(p) and gmpy2.is_prime(q):
            self.p = p
            self.q = q
        else:
            print("[*] 未给定合理的 p 和 q, 程序将自行产生")
            self.p = getPrime(bit_length)
            self.q = getPrime(bit_length)

        self.__create_rsa(e)

    def __generate_e(self):
        """
        生成器, 负责产生合理的 e 值以供选择
        :return: generator
        """
        for e in range(3, self.et):
            if gmpy2.gcd(e, self.et) == 1:
                yield e

    def __create_rsa(self, e):
        """
        产生有关 rsa 的一切参数, 包括 N, phi_N, d, e 等
        :param e: 指定公钥 e
        :return: None
        """
        self.n = self.__compute_n(self.p, self.q)
        self.et = self.__compute_et(self.p, self.q)

        if e:
            self.e = e
            self.d = self.__compute_d(e)
        else:
            # 求 d 的时候, invmod(e, et) 不一定存在, 所以利用循环直到生成合法数值
            for e in self.__generate_e():
                try:
                    self.d = self.__compute_d(e)
                except ZeroDivisionError:
                    # 当前 e 值不合理, 产生下一个 e
                    continue
                else:
                    self.e = e
                    break

    def print_my_rsa(self):
        print("P = {p}\nQ = {q}\nN = {n}\nPhi_N = {et}\nE = {e}\nD = {d}".format(
            p=self.p, q=self.q, n=self.n, et=self.et, e=self.e, d=self.d
        ))

    def encrypt(self, plaintext):
        message = gmpy2.mpz(plaintext, 16)
        return gmpy2.powmod(message, self.e, self.n)

    def decrypt(self, cipher_text):
        cipher_text = gmpy2.mpz(cipher_text)
        return gmpy2.powmod(cipher_text, self.d, self.n)

    @classmethod
    def __compute_n(cls, p, q):
        """
        计算 RSA 参数中的 N
        :param p: 素数 p
        :param q: 素数 q
        :return: p * q
        """
        return gmpy2.mpz(p) * gmpy2.mpz(q)

    @classmethod
    def __compute_et(cls, p, q):
        """
        计算 RSA 参数中的 phi_N
        :param p: 素数 p
        :param q: 素数 q
        :return: (p - 1) * (q - 1)
        """
        return gmpy2.mpz(p - 1) * gmpy2.mpz(q - 1)

    def __compute_d(self, e):
        """
        计算私钥, d = invmod(e, et)(exp, invmod(17,3120) = 2753)
        :param e: 公钥 e
        :return: 私钥 d
        """
        return gmpy2.invert(e, self.et)


if __name__ == "__main__":
    # 产生 RSA
    my_rsa = MyRSA()
    my_rsa.print_my_rsa()

    # 由于所采用的 p 和 q 位数有限(比如说是 512 bits)，所以明文不宜过长（话说本来就不是用来加密长明文的）
    plaintext = b"Remember it need time to run!!!!!!"
    # 测试加密
    cipher_text = my_rsa.encrypt(binascii.hexlify(plaintext))
    # 测试解密
    result = binascii.unhexlify(hex(my_rsa.decrypt(cipher_text))[2:])

    print("*" * 30 + " 分割线 " + "*" * 30)
    print("Plain text is {0}\nCipher text is {1}\nDecrypt text is {2}".format(plaintext, cipher_text, result))
