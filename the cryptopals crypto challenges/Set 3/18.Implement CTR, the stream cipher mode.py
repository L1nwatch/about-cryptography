'''The string:

L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==
... decrypts to something approximating English in CTR mode, which is an AES block cipher mode that turns AES into a stream cipher, with the following parameters:

      key=YELLOW SUBMARINE
      nonce=0
      format=64 bit unsigned little endian nonce,
             64 bit little endian block count (byte count / 16)
CTR mode is very simple.

Instead of encrypting the plaintext, CTR mode encrypts a running counter, producing a 16 byte block of keystream, which is XOR'd against the plaintext.

For instance, for the first 16 bytes of a message with these parameters:

keystream = AES("YELLOW SUBMARINE",
                "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
... for the next 16 bytes:

keystream = AES("YELLOW SUBMARINE",
                "\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00")
... and then:

keystream = AES("YELLOW SUBMARINE",
                "\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")
CTR mode does not require padding; when you run out of plaintext, you just stop XOR'ing keystream and stop generating keystream.

Decryption is identical to encryption. Generate the same keystream, XOR, and recover the plaintext.

Decrypt the string at the top of this function, then use your CTR function to encrypt and decrypt other things.

This is the only block cipher mode that matters in good code.
Most modern cryptography relies on CTR mode to adapt block ciphers into stream ciphers, because most of what we want to encrypt is better described as a stream than as a sequence of blocks. Daniel Bernstein once quipped to Phil Rogaway that good cryptosystems don't need the "decrypt" transforms. Constructions like CTR are what he was talking about.
====================================================================================================================
'''
# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# 这题直接看着write_up写的，里面的struct库可以好好学一下
# CTR就是先对counter加密后再跟明文异或吧，这题反正是这样

import struct
import base64
from Crypto.Cipher import AES
from itertools import zip_longest


def main():
    encryptor = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
    ciphertext = base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")
    blocks = divide_group(ciphertext)
    plaintext = bytes()
    for index in range(len(blocks)):
        intermediary_value = encryptor.encrypt(get_counter(index))
        plaintext += bytes_xor(blocks[index], intermediary_value)

    print(plaintext)


def divide_group(text, size=16):
    """
    :param text: b"12345678"
    :param size: 3
    :return: [b"123", b"456", b"78"]
    """
    args = [iter(text)] * size
    blocks = list()
    for block in zip_longest(*args):
        blocks.append(b"".join( \
            [bytes([value]) for value in block if value is not None]))

    return blocks


def bytes_xor(bytes1, bytes2):
    """
    :param bytes1: b'123'
    :param bytes2: b'123'
    :return: b'\x00\x00\x00'
    """
    return bytes([a ^ b for a, b in zip(bytes1, bytes2)])


def get_counter(num):
    """
    :param num: 1
    :return: b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00"
    """
    return struct.pack("<QQ", 0, num)


if __name__ == "__main__":
    main()

