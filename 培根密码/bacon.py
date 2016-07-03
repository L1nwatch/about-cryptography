#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 关于培根的编码解码
"""
from itertools import zip_longest

__author__ = '__L1n__w@tch'


class Bacon:
    """
    培根类, 包含培根密码的两种映射表, 编码和解码操作, 分组操作等
    """
    bacon_map1 = {
        'a': "AAAAA", 'g': "AABBA", 'n': "ABBAA", 't': "BAABA",
        'b': "AAAAB", 'h': "AABBB", 'o': "ABBAB", '(u/v)': "BAABB",
        'c': "AAABA", '(i/j)': "ABAAA", 'p': "ABBBA", 'w': "BABAA",
        'd': "AAABB", 'k': "ABAAB", 'q': "ABBBB", 'x': "BABAB",
        'e': "AABAA", 'l': "ABABA", 'r': "BAAAA", 'y': "BABBA",
        'f': "AABAB", 'm': "ABABB", 's': "BAAAB", 'z': "BABBB"
    }
    bacon_map1_reverse = dict(zip(bacon_map1.values(), bacon_map1.keys()))

    bacon_map2 = {
        'a': "AAAAA", 'b': "AAAAB", 'c': "AAABA", 'd': "AAABB", 'e': "AABAA",
        'f': "AABAB", 'g': "AABBA", 'h': "AABBB", 'i': "ABAAA", 'j': "ABAAB",
        'k': "ABABA", 'l': "ABABB", 'm': "ABBAA", 'n': "ABBAB", 'o': "ABBBA",
        'p': "ABBBB", 'q': "BAAAA", 'r': "BAAAB", 's': "BAABA", 't': "BAABB",
        'u': "BABAA", 'v': "BABAB", 'w': "BABBA", 'x': "BABBB", 'y': "BBAAA",
        'z': "BBAAB"
    }
    bacon_map2_reverse = dict(zip(bacon_map2.values(), bacon_map2.keys()))

    @staticmethod
    def divide_group(data, block_size):
        """
        对字节流进行分组操作
        :param data: b"abcdefghi"
        :param block_size: 3
        :return: [b"abc", b"def", b"ghi"]
        """
        args = [iter(data)] * block_size

        blocks = []
        for block in zip_longest(*args):
            blocks.append(b"".join([bytes([value]) for value in block]))

        return blocks

    def __init__(self, use_map):
        self.use_map = use_map  # 选择要用哪个映射表
        self.use_map_1 = False  # 是否使用了映射表 1

        if use_map == Bacon.bacon_map1 or use_map == Bacon.bacon_map1_reverse:
            print("[*] 使用映射表 1 可能会导致歧义")
            self.use_map_1 = True

    def encode(self, plaintext):
        """
        编码操作
        :param plaintext: "THEQUICKBR"
        :return: "BAABBAABBBAABAABAAAABABAAABAAAAAABAABABAAAAABBAAAB" or "BAABAAABBBAABAAABBBB(?:u)(?:i)AAABAABAABAAAABBAAAA"
        """
        bacon_encoded = str()
        for char in plaintext.lower():
            try:
                bacon_encoded += self.use_map[char]
            except KeyError:
                bacon_encoded += "(?:{})".format(char)
        return bacon_encoded

    def decode(self, cipher_text):
        """
        解码操作
        :param cipher_text: "BAABBAABBBAABAABAAAABABAAABAAAAAABAABABAAAAABBAAAB"
        :return: "shepticjbq" or "theq(u/v)(i/j)ckbr"
        """
        bacon_decoded = str()
        groups = Bacon.divide_group(str(cipher_text.upper()).encode("utf8"), 5)
        for each in groups:
            try:
                bacon_decoded += self.use_map[each.decode("utf8")]
            except KeyError:
                bacon_decoded += "(?:{})".format(each)

        return bacon_decoded


if __name__ == "__main__":
    bacon = Bacon(Bacon.bacon_map1_reverse)
    print(bacon.decode("baabaaabbbaabaaabbbbbaabbabaaaaaabaabaabaaaabbaaaa"))
    print(bacon.encode("THEQUICKBR"))
