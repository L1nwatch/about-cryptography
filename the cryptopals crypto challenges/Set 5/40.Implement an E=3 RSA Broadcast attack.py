# -*- coding: utf-8 -*-
# version: Python3.X
__author__ = '__L1n__w@tch'

# url: http://cryptopals.com/sets/5/challenges/40/
# 题意: 讲的是如果RSA加密时没有进行填充操作, 会导致漏洞出现
# 现在要求我们重现e=3时的该漏洞, 题目提示说用中国剩余定理
# 步骤:
# 1. 实现中国剩余定理计算函数, 输入参数为三个余数和三个模数, 输出为一个总值
# 2. 实现同一个明文, 三个公钥加密
# 3. 利用中国剩余定理, 在不知道私钥的情况下恢复出明文

import gmpy2
from Crypto.Util.number import getPrime


def test_crt():
    assert (crt((2, 3, 2), (3, 5, 7)) == 23);
    assert (crt((2, 3, 1), (3, 4, 5)) == 11);


def crt(residues, moduli):
    # 中国剩余定理实现参考: https://en.wikipedia.org/wiki/Chinese_remainder_theorem#A_constructive_algorithm_to_find_the_solution
    x = 0
    N = moduli[0] * moduli[1] * moduli[2]
    for i in range(3):
        (_, r, s) = gmpy2.gcdext(moduli[i], N // moduli[i])
        e = s * N // moduli[i]
        x += residues[i] * e

    return x % N


def generate_public_key(bits_length=512, e=3):
    # 注意验证p和q的合法性, 要求与3互质
    while True:
        p = getPrime(bits_length)
        q = getPrime(bits_length)

        if gmpy2.gcd(p, e) == 1 and gmpy2.gcd(q, e) == 1:
            return gmpy2.mpz(p) * gmpy2.mpz(q), e


def rsa_crt_attack(residues, moduli):
    # 算法是题目给的这句:
    # To decrypt RSA using a simple cube root, leave off the final modulus operation;
    result = crt(moduli, [n for n, _ in residues])
    return gmpy2.mpz(gmpy2.mpz(result) ** (1 / 3.0))


def main():
    # 测试中国剩余定理函数是否正确, 测试用的两组数值参考网上资料
    test_crt()

    plaintext = 0x123456789
    public_keys = [generate_public_key(), generate_public_key(), generate_public_key()]
    cipher_text = [gmpy2.powmod(plaintext, e, n) for n, e in public_keys]
    recovered_plaintext = rsa_crt_attack(public_keys, cipher_text)
    print("Raw plaintext: ", plaintext)
    print("Recovered plaintext: ", recovered_plaintext)
    assert (plaintext == recovered_plaintext)


if __name__ == "__main__":
    main()

