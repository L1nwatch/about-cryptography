#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试摩尔斯电码的编码和解码是否正确
"""
import unittest
from morse import Morse

__author__ = '__L1n__w@tch'


class TestMorse(unittest.TestCase):
    def setUp(self):
        self.plaintext = "The quick brown fox jumps over the lazy dog"
        self.cipher_text = r"- .... .  --.- ..- .. -.-. -.-  -... .-. --- .-- -.  ..-. --- -..-  .--- ..- -- .--. ...  --- ...- . .-.  - .... .  .-.. .- --.. -.--  -.. --- --."

    def test_encode(self):
        self.failUnless(Morse.encode_morse(self.plaintext) == self.cipher_text)

    def test_decode(self):
        self.failUnless(Morse.decode_morse(self.cipher_text) == self.plaintext.replace(" ", "").upper())


if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTest(TestMorse("test_encode"))
    suite.addTest(TestMorse("test_decode"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
