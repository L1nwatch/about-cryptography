"""

Fixed XOR

Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

1c0111001f010100061a024b53535009181c

... after hex decoding, and when XOR'd against:

686974207468652062756c6c277320657965

... should produce:

746865206b696420646f6e277420706c6179
"""

# -*- coding: utf-8 -*-
__author__ = 'Lin'

# url: http://cryptopals.com/sets/1/challenges/2/
# 题意: 实现2个十六进制串的异或

import binascii


def test():
    hex1 = "1c0111001f010100061a024b53535009181c"
    hex2 = "686974207468652062756c6c277320657965"
    result = hex_xor(hex1, hex2)
    result_2 = xor(hex1, hex2)
    print(result)
    print(result_2, binascii.hexlify(result_2))


def hex_xor(hex_str1, hex_str2):
    """
    小心精度问题, 精度参考python内置int函数
    :param hex_str1: "1c0111001f010100061a024b53535009181"
    :param hex_str2: "686974207468652062756c6c277320657965"
    :return: "69a96530759875306214cc4892461565e8e4"
    """
    return hex(int(hex_str1, 16) ^ int(hex_str2, 16))[2:]


def xor(hex_str1, hex_str2):
    """
    这样写不用考虑精度了
    :param hex_str1: "1c0111001f010100061a024b53535009181"
    :param hex_str2: "686974207468652062756c6c277320657965"
    :return: "69a96530759875306214cc4892461565e8e4"
    """
    hex_str1 = bytes.fromhex(hex_str1)
    hex_str2 = bytes.fromhex(hex_str2)
    return bytes([x ^ y for (x, y) in zip(hex_str1, hex_str2)])


if __name__ == '__main__':
    test()

"""
【网上的writeUp，内有第二种异或方式】
def mc_part2():
      a = '1c0111001f010100061a024b53535009181c'
      b = '686974207468652062756c6c277320657965'
      aa = bytes.fromhex(a)
      bb = bytes.fromhex(b)
      a_xor_b = bytes.fromhex('746865206b696420646f6e277420706c6179')
      xored = bytes([x^y for (x,y) in zip(aa,bb)]) # 真正的按位异或啊
      assert( xored == a_xor_b ) # 这里最好学一下，用这种方式来针对这种题
"""