# -*- coding: utf-8 -*-
# version: Python3.X
__author__ = '__L1n__w@tch'

# url: http://cryptopals.com/sets/6/challenges/41/
# 题意: 跟上一题有点联系, 也是加密前没有使用填充导致漏洞的出现
# 但是这道题多了个限制, 就是不能加密同一个明文两次(上道题是对同一个密文加密了3次)
# 但同样有漏洞存在, 以下要求我们重现漏洞, 我们不针对明文加密2次，而是针对明文的倍数来加密

import gmpy2
from Crypto.Util.number import getPrime


def create_rsa_keys(bits_length=512, e=65537):
    # 本来想用pycrypto库的RSA来生成的, 但是这个库至少要求1024bits, 还是自己手搓吧
    rsa = dict()
    while True:
        p = getPrime(512)
        q = getPrime(512)

        if gmpy2.gcd(p, e) == 1 and gmpy2.gcd(q, e) == 1:
            break

    rsa["p"] = p
    rsa["q"] = q
    rsa["n"] = p * q
    rsa["phi"] = (p - 1) * (q - 1)
    rsa["d"] = gmpy2.invert(e, rsa["phi"])
    rsa["e"] = e

    return rsa


def rsa_encrypt(plaintext, n, e):
    """
    :param plaintext: b"a"
    :param n: 93549667877193339332139489....
    :param e: 65537
    :return: 2870243652248975232299125265865902758928365307196812395....
    """
    plaintext = int.from_bytes(plaintext, "big")
    return gmpy2.powmod(plaintext, e, n)


def rsa_decrypt(cipher_text, n, d):
    return gmpy2.powmod(cipher_text, d, n)


def rsa_attack(rsa, cipher_text):
    # Let S be a random number > 1 mod N. Doesn't matter what.
    S = 6666

    # 攻击原理: C' = ((S**E mod N) C) mod N, P = P' / S mod N
    attack_num = (gmpy2.powmod(S, rsa["e"], rsa["n"]) * cipher_text) % rsa["n"]
    attack_num = rsa_decrypt(attack_num, rsa["n"], rsa["d"])
    plaintext = (attack_num * gmpy2.invert(S, rsa["n"])) % rsa["n"]

    # 这里假设明文字节不超过1000
    return (int(plaintext).to_bytes(1000, "big")).replace(b"\x00", b"")


def main():
    rsa = create_rsa_keys()
    plaintext = b"I am plaintext"
    cipher_text = rsa_encrypt(plaintext, rsa["n"], rsa["e"])

    recovered_plaintext = rsa_attack(rsa, cipher_text)
    print("Raw plaintext: ", plaintext)
    print("Recovered plaintext: ", recovered_plaintext)
    assert (plaintext == recovered_plaintext)


if __name__ == "__main__":
    main()

