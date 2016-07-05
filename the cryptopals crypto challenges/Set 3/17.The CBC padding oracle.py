'''
This is the best-known attack on modern block-cipher cryptography.

Combine your padding code and your CBC code to write two functions.

The first function should select at random one of the following 10 strings:

MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93
... generate a random AES key (which it should save for all future encryptions), pad the string out to the 16-byte AES block size and CBC-encrypt it under that key, providing the caller the ciphertext and IV.

The second function should consume the ciphertext produced by the first function, decrypt it, check its padding, and return true or false depending on whether the padding is valid.

What you're doing here.
This pair of functions approximates AES-CBC encryption as its deployed serverside in web applications; the second function models the server's consumption of an encrypted session token, as if it was a cookie.

It turns out that it's possible to decrypt the ciphertexts provided by the first function.

The decryption here depends on a side-channel leak by the decryption function. The leak is the error message that the padding is valid or not.

You can find 100 web pages on how this attack works, so I won't re-explain it. What I'll say is this:

The fundamental insight behind this attack is that the byte 01h is valid padding, and occur in 1/256 trials of "randomized" plaintexts produced by decrypting a tampered ciphertext.

02h in isolation is not valid padding.

02h 02h is valid padding, but is much less likely to occur randomly than 01h.

03h 03h 03h is even less likely.

So you can assume that if you corrupt a decryption AND it had valid padding, you know what that padding byte is.

It is easy to get tripped up on the fact that CBC plaintexts are "padded". Padding oracles have nothing to do with the actual padding on a CBC plaintext. It's an attack that targets a specific bit of code that handles decryption. You can mount a padding oracle on any CBC block, whether it's padded or not.
==================================================================================================================
'''
# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# 写出了第一个和第二个函数，不知道他要干啥，参考write_up了
# 好吧，接下来干的事情和密码学视频第4周的编程作业一样
# 这里学答案的，只做第一个分区的破解（利用iv + 第一个分区）

import random
import string
from Crypto.Cipher import AES


def main():
    global key
    key = prf(16)
    ciphertext = first_function()
    second_function(ciphertext)
    plaintext = attack(ciphertext)
    print(plaintext)


def prf(size=16):
    """
    :param size: 16
    :return: such as b'\x01' * 16
    """
    return b"".join(random.sample([bytes([value]) for value in range(256)], size))


def get_strings():
    strings = """MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"""
    return strings.split("\n")


def first_function():
    """
    :return: b'16 bit iv' + b'ciphertext'
    """
    plaintext = random.choice(get_strings())
    ciphertext = encrypt(plaintext)
    return ciphertext


def encrypt(plaintext):
    """
    :param plaintext: 'plaintext'
    :return: b'16 bit iv' + b'ciphertext'
    """
    iv = prf(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = encryptor.encrypt(pad(bytes(plaintext, "ascii")))  # 不需要codecs库
    return iv + ciphertext


def second_function(ciphertext):
    """
    :param ciphertext: b'ciphertext'
    :return: True or False
    """
    plaintext = decrypt(ciphertext)
    return is_valid_padding(plaintext)


def is_valid_padding(plaintext):
    """
    这里可以改进下，利用前面做过的检测是否合法然后抛出异常的函数，我们捕获异常然后返回bool
    :param plaintext:  b'plaintext'
    :return: True or False
    """

    if len(plaintext) % 16 != 0:
        return False

    padding_value = plaintext[-1]
    if plaintext[-padding_value:] != bytes([padding_value]) * padding_value:
        return False

    return True


def decrypt(ciphertext):
    """
    :param ciphertext: b'16 bit iv' + b'ciphertext'
    :return: b'plaintext'
    """
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    decryptor = AES.new(key, AES.MODE_CBC, iv)
    plaintext = decryptor.decrypt(ciphertext)
    return plaintext


def pad(plaintext, block_size=16):
    """
    :param plaintext: b'abc'
    :param block_size: 5
    :return: b'abc\x02\x02'
    """
    padding_value = block_size - len(plaintext) % block_size
    return plaintext + bytes([padding_value]) * padding_value


def attack(ciphertext):
    """
    :param ciphertext: b'16 bit iv' + b'ciphertext'
    :return: 'plaintext'
    """
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:32]  # 这里只解密第一个分区的明文
    plaintext = ""
    for index in reversed(range(16)):
        value = get_valid_padding_ciphertext(plaintext, index, iv)
        attack_ciphertext = bytearray(iv[:index + 1] + value + ciphertext)
        for guess in string.printable:
            attack_ciphertext[index] = ord(guess) ^ iv[index] ^ (16 - index)
            if second_function(bytes(attack_ciphertext)) is True:
                plaintext = guess + plaintext
                break

    return plaintext


def get_valid_padding_ciphertext(plaintext, index, iv):
    """
    :param plaintext: "g"
    :param index: 14
    :param iv: b' 16 bit iv'
    :return: b'M'
    """
    output = b""

    for i in range(len(plaintext)):
        output = bytes([ord(plaintext[-(i + 1)]) ^ iv[-(i + 1)] ^ (16 - index)]) + output

    return output


if __name__ == "__main__":
    main()



