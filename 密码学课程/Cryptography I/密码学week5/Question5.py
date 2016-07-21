# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'


def main():
    (a, b) = get_a_b()
    print("a = {0}, b = {1}".format(a, b))


def get_a_b():
    """
    :return: (a, b) = (10, -3)
    """
    for a in range(0, 256):
        for b in range(-256, 256):
            if 7 * a + 23 * b == 1:
                return a, b


if __name__ == "__main__":
    main()

