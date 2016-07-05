'''
Now that you have ECB and CBC working:

Write a function to generate a random AES key; that's just 16 random bytes.

Write a function that encrypts data under an unknown key --- that is, a function that generates a random key and encrypts under it.

The function should look like:

encryption_oracle(your-input)
=> [MEANINGLESS JIBBER JABBER]
Under the hood, have the function append 5-10 bytes (count chosen randomly) before the plaintext and 5-10 bytes after the plaintext.

Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC the other half (just use random IVs each time for CBC). Use rand(2) to decide which to use.

Detect the block cipher mode the function is using each time. You should end up with a piece of code that, pointed at a block box that might be encrypting ECB or CBC, tells you which one is happening.
'''
# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# 看了半天，题目要求是啥啊没太看懂，一步一步写吧
# 到后面有点卡住，所以参考了下write_up的思路写的
# 探测是否为ECB模式可以参考Set1的challenge8

import random
import codecs
from Crypto.Cipher import AES
from itertools import zip_longest
from collections import Counter


def main():
    plaintext = "plaintext" * 160
    (mode, ciphertext) = encrypt_oracle(plaintext)
    print("mode use:{0}, guess mode:{1}".format(mode, "ECB" if is_using_ecb(ciphertext) else "CBC"))


def prf(key_size=16):
    """
    Write a function to generate a random AES key; that's just 16 random bytes.
    :param key_size: 3
    :return: b'a0D'
    """

    key = b"".join([bytes([value]) for value in random.sample(range(256), key_size)])
    return key


def encrypt_oracle(data):
    """
    :param data: "plaintext"
    :return: "CBC", b"ciphertext"
    """
    size = 16

    key = prf(size)
    plaintext = codecs.encode(data, "ascii")

    plaintext = prf(random.randint(5, 10)) + plaintext + prf(random.randint(5, 10))
    plaintext = pad(plaintext, size)
    choice = random.choice([AES.MODE_CBC, AES.MODE_ECB])
    if choice == AES.MODE_CBC:
        iv = prf(size)
        encryptor = AES.new(key, AES.MODE_CBC, IV=iv)
    elif choice == AES.MODE_ECB:
        encryptor = AES.new(key, AES.MODE_ECB)

    mode = {AES.MODE_CBC: "CBC", AES.MODE_ECB: "ECB"}
    ciphertext = encryptor.encrypt(plaintext)

    return mode[choice], ciphertext


def pad(plaintext, size=16):
    """input: plaintext=b"abcdefg", block_size=10
       output: b"abcdefg\x03\x03\x03"."""
    padding_value = size - len(plaintext) % size
    output = plaintext + bytes([padding_value]) * padding_value
    return output


def is_using_ecb(ciphertext):
    """
    :param ciphertext: b'a' * 2000
    :return: True
    """
    blocks = divide_group(ciphertext, 16)

    return Counter(blocks).most_common()[0][1] > 1


def divide_group(data, block_size):
    """
    :param data: b"abcdefghi"
    :block_size: 3
    :return: [b"abc", b"def", b"ghi"]
    """
    args = [iter(data)] * block_size

    blocks = []
    for block in zip_longest(*args):
        blocks.append(b"".join([bytes([value]) for value in block]))

    return blocks


if __name__ == "__main__":
    main()

