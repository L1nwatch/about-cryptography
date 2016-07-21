# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# 自己算不出私钥d，查看了一下write_up
# 发现write_up是用gmpy2.invert（模逆运算）,学习了~~
# 本来想用crypto.Publickey自带的RSA库来解的，发现有点不会用啊。所以学着答案自己解了

import gmpy2
import binascii


def main():
    ciphertext = "22096451867410381776306561134883418017410069787892831071" \
                 "73183914367613560012053800428232965047350942434394621975" \
                 "15122564658399679428894607645420405815647489880137348641" \
                 "20452325229320176487916666402997509188729971690526083222" \
                 "06777160001932926087000957999372407745896777369781757126" \
                 "7229951148662959627934791540"

    N = "17976931348623159077293051907890247336179769789423065727343008115" \
        "77326758055056206869853794492129829595855013875371640157101398586" \
        "47833778606925583497541085196591615128057575940752635007475935288" \
        "71082364994994077189561705436114947486504671101510156394068052754" \
        "0071584560878577663743040086340742855278549092581"
    e = 65537
    pk, sk = get_keys(N, e)
    plaintext = decrypt_RSA(ciphertext, sk)
    print(decode_PKCS1(plaintext))


def get_keys(N, e):
    """
    :param N: 112345136...
    :param e: 65537
    :return: pk = (N, e), sk = (N, d)
    """
    p, q = factor(N)
    Phi_N = (p - 1) * (q - 1)
    d = gmpy2.invert(e, Phi_N)
    return (N, e), (N, d)


def factor(N):
    """
    :param N: 123412421....
    :return: mpz(p), mpz(q)
    """
    N = gmpy2.mpz(N)
    A = gmpy2.isqrt(N) + 1  # 这里得用isqrt,用sqrt的话返回的是一个合理的mpfr值
    x = gmpy2.isqrt(A ** 2 - N)
    p = A - x
    q = A + x
    return p, q


def decrypt_RSA(ciphertext, sk):
    """
    :param ciphertext: "123231321....."
    :param sk: (N, d)
    :return: hex(plaintext)[2:]
    """
    N = gmpy2.mpz(sk[0])
    d = gmpy2.mpz(sk[1])
    ciphertext = gmpy2.mpz(ciphertext)
    return hex(gmpy2.powmod(ciphertext, d, N))[2:]


def decode_PKCS1(plaintext):
    """
    这道题用00作为分割符
    :param ciphertext: "16 hex value"
    :return: b"plaintext"
    """
    plaintext = plaintext[plaintext.find("00") + 2:]
    return binascii.unhexlify(plaintext)


if __name__ == "__main__":
    main()