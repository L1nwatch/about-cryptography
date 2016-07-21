# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# a * x + b = 0 in ZN
# x = -b * inverse_a in ZN

def main():
    a, b, n = 3, -5, 19
    inverse_a = get_i_j(a, n)[0]
    answer = (-b * inverse_a) % n
    print(answer)


def get_i_j(a, n):
    for i in range(256):
        for j in range(-256, 256):
            if i * a + n * j == 1:
                print(i, j)
                return i, j


if __name__ == "__main__":
    main()

