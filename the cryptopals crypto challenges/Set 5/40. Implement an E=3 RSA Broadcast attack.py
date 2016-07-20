#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
Assume you're a Javascript programmer. That is, you're using a naive handrolled RSA to encrypt without padding.

Assume you can be coerced into encrypting the same plaintext three times, under three different public keys.
You can; it's happened.

Then an attacker can trivially decrypt your message, by:

Capturing any 3 of the ciphertexts and their corresponding pubkeys
Using the CRT to solve for the number represented by the three ciphertexts
(which are residues mod their respective pubkeys)

Taking the cube root of the resulting number
The CRT says you can take any number and represent it as the combination of a series of residues mod a series of moduli.
 In the three-residue case, you have:

result =
  (c_0 * m_s_0 * invmod(m_s_0, n_0)) +
  (c_1 * m_s_1 * invmod(m_s_1, n_1)) +
  (c_2 * m_s_2 * invmod(m_s_2, n_2)) mod N_012
where:

 c_0, c_1, c_2 are the three respective residues mod
 n_0, n_1, n_2

 m_s_n (for n in 0, 1, 2) are the product of the moduli
 EXCEPT n_n --- ie, m_s_1 is n_0 * n_2

 N_012 is the product of all three moduli
To decrypt RSA using a simple cube root, leave off the final modulus operation; just take the raw accumulated result
and cube-root it.

# 题意
讲的是如果 RSA 加密时没有进行填充操作, 会导致漏洞出现

现在要求我们重现 e = 3 时的该漏洞, 题目提示说用中国剩余定理

# 步骤
1. 实现中国剩余定理计算函数, 输入参数为三个余数和三个模数, 输出为一个总值
2. 实现同一个明文, 三个公钥加密
3. 利用中国剩余定理, 在不知道私钥的情况下恢复出明文
"""
import gmpy2
import random
from Crypto.Util.number import getPrime

__author__ = '__L1n__w@tch'


def check_crt_algorithm():
    """
    验证所实现的中国剩余定理算法是否正确
    :return:
    """
    assert (crt((2, 3, 2), (3, 5, 7)) == 23);
    assert (crt((2, 3, 1), (3, 4, 5)) == 11);


def crt(residues, moduli):
    """
    实现中国剩余定理, 参考
        https://en.wikipedia.org/wiki/Chinese_remainder_theorem#A_constructive_algorithm_to_find_the_solution
    :param residues:
    :param moduli:
    :return:
    """
    x = 0
    N = moduli[0] * moduli[1] * moduli[2]
    for i in range(3):
        (_, r, s) = gmpy2.gcdext(moduli[i], N // moduli[i])
        e = s * N // moduli[i]
        x += residues[i] * e

    return x % N


def generate_public_key(bits_length=512, e=3):
    """
    产生关于 RSA 的合法参数, p, q, e
    :param bits_length: 所需的 p 和 q 要求的位长度
    :param e: 3
    :return: n, e
    """
    # 注意验证参数的合法性, 要求 phi(N) 与 e 互素
    while True:
        p = getPrime(bits_length)
        q = getPrime(bits_length)
        n = gmpy2.mpz(p) * gmpy2.mpz(q)
        phi_n = gmpy2.mpz(p - 1) * gmpy2.mpz(q - 1)

        if gmpy2.gcd(phi_n, e) == 1:
            return n, e


def rsa_crt_attack(residues, moduli):
    """
    根据题目给的公式, 利用中国剩余定理还原得到明文
    :param residues: 余数
    :param moduli: 模数
    :return: 破解得到的明文值
    """
    # 算法是题目给的这句:
    # To decrypt RSA using a simple cube root, leave off the final modulus operation;
    result = crt(moduli, [n for n, _ in residues])  # 只要留下 n 即可
    return gmpy2.mpz(gmpy2.mpz(result) ** (1 / 3))  # 这里存在精度误差


if __name__ == "__main__":
    # 测试中国剩余定理函数是否正确, 测试用的两组数值参考网上资料
    check_crt_algorithm()

    plaintext = random.randint(0, 2 ** 32)  # 随机产生一个明文
    public_keys = [generate_public_key(), generate_public_key(), generate_public_key()]  # 多对公钥
    cipher_text = [gmpy2.powmod(plaintext, e, n) for n, e in public_keys]  # 多对公钥对同一明文的加密结果

    recovered_plaintext = rsa_crt_attack(public_keys, cipher_text) + 1  # 存在浮点数精度误差
    print("Raw plaintext: ", plaintext)
    print("Recovered plaintext: ", recovered_plaintext)
    assert plaintext == recovered_plaintext
