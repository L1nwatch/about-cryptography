#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 摩尔斯电码的编码和解码操作

注意 H 和 & 重复了?
"""
from collections import ChainMap

__author__ = '__L1n__w@tch'


class Morse:
    """
    摩尔斯电码的类, 包括了映射表, 编码函数与解码函数
    """
    upper_letters_map = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..",
        "E": ".", "F": "..-.", "G": "--.", "H": "....",
        "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
        "M": "--", "N": "-.", "O": "---", "P": ".--.",
        "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
        "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
        "Y": "-.--", "Z": "--.."}

    digits_map = {
        "0": "-----", "1": ".----", "2": "..---", "3": "...--",
        "4": "....-", "5": ".....", "6": "-....", "7": "--...",
        "8": "---..", "9": "----."
    }

    symbols_map = {
        ".": ".-.-.-", ":": "---...", ",": "--..--", ";": "-.-.-.",
        "?": "..--..", "=": "-...-", "'": ".----.", "/": "-..-.",
        "!": "-.-.--", "-": "-....-", "_": "..--.-", "\"": ".-..-.",
        "(": "-.--.", ")": "-.--.-", "$": "...-..-", "@": ".--.-."
        # 这个与 H 重复了: "&": "...."
    }

    # 合并多个字典, 这样不会产生新的字典, 而且这样的字典会随原字典的改变而改变
    all_map = ChainMap(upper_letters_map, digits_map, symbols_map)

    @staticmethod
    def reverse_map(a_map):
        """
        把映射表转换一下, 比如说原来映射关系是 "A":".-", 转换后变成 ".-":"A"
        :param a_map: {"A": ".-", "B": "-..."}
        :return: {".-": "A", "-...": "B"}
        """
        return dict(zip(a_map.values(), a_map.keys()))

    @staticmethod
    def decode_morse(cipher_text):
        """
        对摩尔斯电码进行解码操作
        :param cipher_text: "-- --- .-. ... . 你好"
        :return: "MORSE你好"
        """
        groups = cipher_text.split(" ")
        all_map = Morse.reverse_map(Morse.all_map)
        morse_decoded = str()
        for each in groups:
            try:
                morse_decoded += all_map[each]
            except KeyError:
                morse_decoded += each

        return morse_decoded

    @staticmethod
    def encode_morse(plain_text):
        """
        对明文进行摩尔斯电码编码操作
        :param plain_text: "你好12345678"
        :return: "你好.---- ..--- ...-- ....- ..... -.... --... ---.."
        """
        morse_encoded = str()
        for char in plain_text.upper():
            try:
                morse_encoded += Morse.all_map[char] + " "
            except KeyError:
                morse_encoded += char
        return morse_encoded[:-1]


if __name__ == "__main__":
    print("测试解码: {}".format(Morse.decode_morse("-- --- .-. ... . 你好")))
    print("测试编码: {}".format(Morse.encode_morse("你好12345678")))
