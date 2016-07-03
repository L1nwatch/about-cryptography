#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试凯撒密码的加解密
"""
import unittest
from caesar_cipher import Caesar

__author__ = '__L1n__w@tch'


class TestCaesar(unittest.TestCase):
    def setUp(self):
        self.test_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        self.shift = 28
        self.answer_string = "cdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZab"

    def test_caesar(self):
        caesar = Caesar(self.test_string)
        cipher_text = caesar.encrypt(self.test_string, self.shift)
        self.failUnless(cipher_text == self.answer_string)
        plaintext = caesar.decrypt(self.answer_string, self.shift)
        self.failUnless(plaintext == self.test_string)


if __name__ == "__main__":
    unittest.main()
