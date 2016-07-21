# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'


def main():
    N = 35
    List = []
    for i in range(1, N):
        if gcd(i, N) == 1:
            List.append(i)

    print(List)
    print(len(List))


def gcd(x, y):
    return x if y == 0 else gcd(y, x % y)


if __name__ == "__main__":
    main()

