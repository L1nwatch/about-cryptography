"""

Single-byte XOR cipher

The hex encoded string:

1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.
Achievement Unlocked

You now have our permission to make "ETAOIN SHRDLU" jokes on Twitter.
"""

# -*- coding: utf-8 -*-
__author__ = 'Lin'

# 以下测试hex与ascii的相互转换

import codecs
import binascii


def test():
    # todo
    test_hex = "7061756c"
    test_ascii = "paul"

    get_ascii = codecs.decode(test_hex, 'hex')  # 这个可以直接把hex转成ascii
    get_hex = binascii.hexlify(bytes(test_ascii, 'ascii'))  # 这个可以直接把ascii转成hex

    print(get_ascii)
    print(get_hex)

    print(codecs.decode(get_ascii, "ascii"))  # 把bytes型的ascii码转成字符串型的ascii
    print(get_hex.decode("utf-8")) # 把bytes型的hex转成字符串型的hex


def main():
    hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    b_hex = codecs.decode(hex_string, 'hex')
    characters = "abcdefghijklmnopqrstuvwxyz"
    for ch in characters:
        print(ch)
        for each in b_hex:
            print(chr(ord(ch) ^ each), end='')  # 自己的异或法其实好像有点问题，有些东西好像不太对的
        print("")


if __name__ == '__main__':
    # main()
    test()

    # print(binascii.unhexlify(test_hex))


"""
【网上的writeUp，写得很不错，以后都跟他一样按位异或了！：】
import string # 这个库保存了ascii常量，以后就不用手打了


def mc_part3(idx=15):
    h = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    hh = bytes.fromhex(h)

    for k in string.ascii_letters:
        print(k)
        # 这里按位异或的方法很好啊，而且用到了列表推导式最后又全部转为了位! 好强大
        print(bytes([a ^ b for (a, b) in zip(hh, bytes(k * len(hh), 'ascii'))])) # k * len(hh)是把字母重复了长度次


if __name__ == '__main__':
    mc_part3()


"""