#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 解密摩斯电码
"""

__author__ = '__L1n__w@tch'

# 思路
# 定义一个全局的字典，里面包含所有的morse_code
morse_code = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h',
              '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p',
              '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
              '-.--': 'y', '--..': 'z'}  # dict


def get_morse_code(string):
    list_new = list(string.split('  '))
    for i in list_new:
        print(morse_code[i], end='')


string1 = str("--  ---  .-.  ...  .")
string2 = str("-.-.  ---  -..  .")
get_morse_code(string1)
get_morse_code(string2)
