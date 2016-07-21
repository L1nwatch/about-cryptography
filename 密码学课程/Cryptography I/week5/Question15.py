# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

import math


def main():
    prime_list = create_prime_list(100)
    for p in prime_list:
        print("prime is {0}, num of generators is {1}".format(p, count_generators(p)))
        print("num is {0}, num of count is {1}".format(p - 1, count_num(p - 1)))


def create_prime_list(max_num):
    """
    :max_num: 100
    :return: prime_list = [2, 3, 5, 7, ...]
    """
    prime_list = []
    for i in range(2, max_num):
        if is_prime(i) is True:
            prime_list.append(i)

    return prime_list


def is_prime(num):
    """
    :param num: 3
    :return: True
    """
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False

    return True


def count_generators(prime):
    """
    :param prime: 3
    :return: 1
    """
    counts = 0
    for i in range(prime):
        if is_generator(i, prime) is True:
            counts += 1

    return counts


def is_generator(num, prime):
    """
    :param num: 2, 3
    :return: True
    """
    Set = set()
    for i in range(1, 256):
        Set.update(set([num ** i % prime]))

    if len(Set) == (prime - 1):
        return True
    else:
        return False


def count_num(N):
    counts = 0
    for i in range(1, N):
        if gcd(i, N) == 1:
            counts += 1

    return counts


def gcd(x, y):
    return x if y == 0 else gcd(y, x % y)


if __name__ == "__main__":
    main()

