#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
Here is the opening stanza of an important work of the English language:
    Burning 'em, if you ain't quick and nimble
    I go crazy when I hear a cymbal
Encrypt it, under the key "ICE", using repeating-key XOR.
In repeating-key XOR, you'll sequentially apply each byte of the key; the first byte of plaintext will be XOR'd
against I, the next C, the next E, then I again for the 4th byte, and so on.
It should come out to:
    0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
    a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f
Encrypt a bunch of stuff using your repeating-key XOR function. Encrypt your mail. Encrypt your password file.
Your .sig file. Get a feel for it. I promise, we aren't wasting your time with this.

# 思路
与第 3 题和第 4 题思路一样, 只不过异或的字节流不再是由单个字符产生的
"""

__author__ = '__L1n__w@tch'


def xor(ascii_str, key_str):
    """
    对两个字符串进行异或操作, 返回十六进制的异或结果
    :param ascii_str: "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    :param key_str: "ICE"
    :return: "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a2622632427276527" \
             "2a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    """
    ascii_str = bytes(ascii_str, "ascii")
    key_str = bytes(key_str, "ascii")
    after_xor = str()
    for i in range(len(ascii_str)):
        # zfill是为了保证0xb的时候能表示为0x0b
        after_xor += hex(ascii_str[i] ^ key_str[i % len(key_str)])[2:].zfill(2)

    return after_xor


def writeup(ascii_str, key_str, answer):
    """
    这是网上的 writeup, 特点是利用了生成器来产生待异或的 key
    :param ascii_str: "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    :param key_str: 'ICE'
    :param answer: "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a2622632427276527" \
                   "2a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    :return: None
    """

    def cycle_key(key):
        """
        产生循环的 key
        :param key:
        :return:
        """
        idx = 0
        while True:
            yield ord(key[idx % len(key)])  # 带有 yield 的函数在 Python 中被称之为 generator（生成器）
            idx += 1

    g = cycle_key('ICE')
    s = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    hh = bytes(s, 'ascii')
    xored = bytes([a ^ b for (a, b) in zip(hh, g)])

    c = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
    expected = bytes.fromhex(c)
    assert (xored == expected)


if __name__ == "__main__":
    key = "ICE"
    plaintext = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
    answer = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a2622632427276527" \
             "2a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    assert answer == xor(plaintext, key)
    writeup(plaintext, key, answer)
