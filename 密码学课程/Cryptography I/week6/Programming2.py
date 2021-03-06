# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

import gmpy2


def main():
    N = "6484558428080716696628242653467722787263437207069762630604390703787" \
        "9730861808111646271401527606141756919558732184025452065542490671989" \
        "2428844841839353281972988531310511738648965962582821502504990264452" \
        "1008852816733037111422964210278402893076574586452336833570778346897" \
        "15838646088239640236866252211790085787877"

    p, q = factor(N)
    print("p = {0}\nq = {1}".format(p, q))


def factor(N):
    """
    :param N: mpz(6)
    :return : mpz(p), mpz(q)
    """
    N = gmpy2.mpz(N)
    for i in range(1, 2 ** 20):
        A = gmpy2.isqrt(N) + i  # 注意i得从1开始，0会报错，原因未知
        x = gmpy2.isqrt(A ** 2 - N)
        p = A - x
        q = A + x
        if p * q == N:
            return p, q


if __name__ == "__main__":
    main()