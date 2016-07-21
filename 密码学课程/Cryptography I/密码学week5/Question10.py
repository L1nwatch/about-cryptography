# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'


def main():
    g, N = 2, 35
    order = get_order(g, N)
    print(order)


def get_order(g, N):
    """
    :param g: 2
    :param N: 35
    :return: 12
    """
    Set = set()
    for i in range(128):
        num = (g ** i) % N
        if num not in Set:
            Set.update(set([num]))

    print(Set)
    return len(Set)


if __name__ == "__main__":
    main()

