'''
Implement CBC mode
CBC mode is a block cipher mode that allows us to encrypt irregularly-sized messages, despite the fact that a block cipher natively only transforms individual blocks.

In CBC mode, each ciphertext block is added to the next plaintext block before the next call to the cipher core.

The first plaintext block, which has no associated previous ciphertext block, is added to a "fake 0th ciphertext block" called the initialization vector, or IV.

Implement CBC mode by hand by taking the ECB function you wrote earlier, making it encrypt instead of decrypt (verify this by decrypting whatever you encrypt to test), and using your XOR function from the previous exercise to combine them.

The file here is intelligible (somewhat) when CBC decrypted against "YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)

Don't cheat.
Do not use OpenSSL's CBC code to do CBC mode, even to verify your results. What's the point of even doing this stuff if you aren't going to learn from it?
'''
# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# 看题目描述不知道那串yellow是干啥的，看完writeUp才知道是key....
# 每一行读取一下，发现每一行才61个字符，所以肯定是整个数据来进行加密解密的
# 自己写的解出来是乱码，然后发现原来文件是base64过的而不是ascii的，好吧

from Crypto.Cipher import AES
from itertools import zip_longest
import base64


def main():
    key = "YELLOW SUBMARINE"
    iv = b'\x00' * 16
    file_name = "task10.txt"
    lines = get_file_content(file_name)
    ciphertext = b"".join([base64.b64decode(l.strip()) for l in lines])
    plaintext = decrypt(key, iv, ciphertext)
    print(plaintext)


def get_file_content(file_name):
    """input: file_name = "task10.txt"
       output: lines = ["line1\n", "line2\n", "line3\n", ...]"""
    with open(file_name, "rU") as f:
        lines = f.readlines()

    return lines


def decrypt(key, iv, ciphertext):
    """
    :param key: "YELLOW SUBMARINE"
    :param iv: b'\x00' * 16
    :param ciphertext: b"ciphertext"
    :return: "plaintext"
    """
    block_size = 16
    decryptor = AES.new(key, AES.MODE_ECB)  # 题目要求自己用ECB实现CBC吧
    blocks = divide_group(ciphertext, block_size)
    blocks.insert(0, iv)

    plaintext = b""
    for index in range(1, len(blocks)):
        tmp = decryptor.decrypt(blocks[index])
        plaintext += byte_xor(tmp, blocks[index - 1])

    return plaintext.decode("utf-8")


def divide_group(ciphertext, block_size):
    """
    :param ciphertext: b'abcdefghi'
    :param block_size: 3
    :return: [b"abc", b"def", b"ghi"]
    """
    if len(ciphertext) % block_size != 0:
        raise ValueError

    args = [iter(ciphertext)] * block_size

    blocks = []
    for each_block in zip_longest(*args):
        blocks.append(b"".join([bytes([value]) for value in each_block]))

    return blocks


def byte_xor(string1, string2):
    """
    :param string1: b'1234567'
    :param string2: b'1234567'
    :return: b'\x00\x00\x00\x00\x00\x00\x00'
    """
    return bytes([a ^ b for a, b in zip(string1, string2)])


if __name__ == "__main__":
    main()

