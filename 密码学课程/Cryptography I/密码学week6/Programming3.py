# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# =============================================================================
# 这题自己做不出来，或者说是懒得去推导数学公式。
# 以下是write_up的解释，清楚明了：
# let M = (3p+2q)/2
# M is not an integer since 3p + 2q is odd
# So there is some integer A = M + 0.5 and some integer i such that
# 3p = M + i - 0.5 = A + i - 1
# and
# 2q = M - i + 0.5 = A - i
#
# N = pq = (A-i)(A+i-1)/6 = (A^2 - i^2 - A + i)/6
# So 6N = A^2 - i^2 - A + i
# i^2 - i = A^2 - A - 6N
# =============================================================================

import gmpy2


def main():
    N = "72006226374735042527956443552558373833808445147399984182665305798191" \
        "63556901883377904234086641876639384851752649940178970835240791356868" \
        "77441155132015188279331812309091996246361896836573643119174094961348" \
        "52463970788523879939683923036467667022162701835329944324119217381272" \
        "9276147530748597302192751375739387929"
    p, q = factor(N)
    print("p = {0}\nq = {1}".format(p, q))


def factor(N):
    """
    :param N: mpz(N)
    :return: mpz(p), mpz(q)
    """
    N = gmpy2.mpz(N)
    A = ceil_sqrt(6 * N)
    a = 1
    b = -1
    c = -(A ** 2 - A - 6 * N)
    det = b ** 2 - 4 * a * c
    roots = (gmpy2.div(-b + gmpy2.isqrt(det), 2 * a), # 这里还非得用isqrt不能用sqrt了
             gmpy2.div(-b - gmpy2.isqrt(det), 2 * a))

    for x in roots:
        p = (A - x) // 3
        q = (A + x - 1) // 2
        if p * q == N:
            return p, q


def ceil_sqrt(num):
    """
    # 参考答案写了这么一个函数，觉得挺好用的
    :param num: mpz(num)
    :return: mpz(res)
    """
    num = gmpy2.mpz(num)
    r, i = gmpy2.isqrt_rem(num)
    res = r + (1 if i else 0 )
    return res


if __name__ == "__main__":
    main()

