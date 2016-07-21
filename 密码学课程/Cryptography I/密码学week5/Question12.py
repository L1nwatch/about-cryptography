# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'


def main():
    a, b, c, p = 1, 4, 1, 23
    inverse_2a = get_inverse_a(a, p)
    square_root = get_square_root(b ** 2 - 4 * a * c, p)

    solution = []
    solution.append((-b + square_root[0]) * inverse_2a[0])
    solution.append((-b + square_root[1]) * inverse_2a[0])
    solution.append((-b - square_root[0]) * inverse_2a[0])
    solution.append((-b - square_root[1]) * inverse_2a[0])
    print(solution)

    for each in solution:
        num = (a * (each ** 2) + b * each + c ) % p
        print(num)


def get_inverse_a(a, N):
    """
    :param a: 1
    :param N: 23
    :return: (12, -1)
    """

    for i in range(256):
        for j in range(-256, 256):
            if i * (2 * a) + j * N == 1:
                return (i, j)


def get_square_root(a, N):
    """
    :param a: 12
    :param N: 23
    :return: [9, 14]
    """
    dictionary = dict()
    for i in range(N):
        dictionary.setdefault(i, i ** 2 % N)

    square_root = []
    for key, value in dictionary.items():
        if value == a:
            square_root.append(key)

    return square_root


if __name__ == "__main__":
    main()

