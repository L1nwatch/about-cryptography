# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

import binascii


def main():
    plaintext = "attack at dawn"
    ciphertext = "6c73d5240a948c86981bc294814d"
    target_plaintext = "attack at dusk"
    key = bytes_xor(plaintext.encode("ascii"), binascii.unhexlify(ciphertext))
    target_ciphertext = bytes_xor(key, target_plaintext.encode("ascii"))
    print(binascii.hexlify(target_ciphertext))


def bytes_xor(bytes1, bytes2):
    """
    :param bytes1: b'123'
    :param bytes2: b'123'
    :return: b'\x00\x00\x00'
    """
    return bytes([a ^ b for a, b in zip(bytes1, bytes2)])


if __name__ == "__main__":
    main()

