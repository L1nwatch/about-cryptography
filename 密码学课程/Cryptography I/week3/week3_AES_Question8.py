# -*- coding: utf-8 -*-
__author__ = 'Lin'

from Crypto.Cipher import AES

"""
python2.X 版本的
def main():
    x1 = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF".decode(
        'hex')  # arbitrary 128bit string
    y1 = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF".decode(
        'hex')  # arbitrary 128bit string
    y2 = "00000000000000000000000000000000".decode('hex')  # 0^n string

    print "x1:", x1.encode('hex')
    print "y1:", y1.encode('hex')
    print "y2:", y2.encode('hex')

    m1 = f1(x1, y1)
    print "\nf1(x1,y1) = ", m1.encode('hex')

    x2 = find_x2(m1, y2)
    print "\nD(y2, f1(x1,y1)) => x2:", x2.encode('hex')

    m2 = f1(x2, y2)
    print "\n\ncheck: f1(x2,y2) =", m2.encode('hex'), "\n==", m1.encode('hex'), "? ", m1 == m2

    print "\n"
"""


def main():
    key = b"FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    plaintext = b"FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"

    ciphertext = AES.new(key, AES.MODE_ECB).encrypt(plaintext)

    print(ciphertext)


def f1(x, y):
    return strxor(AES.new(y, AES.MODE_ECB).encrypt(x), y)


def find_x2(m, y):
    return AES.new(y, AES.MODE_ECB).decrypt(m)


# xor two strings of different lengths
def strxor(a, b):
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


if __name__ == '__main__':
    main()


