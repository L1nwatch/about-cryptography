"""A block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of plaintext into ciphertext. But we almost never want to transform a single block; we encrypt irregularly-sized messages.

One way we account for irregularly-sized messages is by padding, creating a plaintext that is an even multiple of the blocksize. The most popular padding scheme is called PKCS#7.

So: pad any block to a specific block length, by appending the number of bytes of padding to the end of the block. For instance,

"YELLOW SUBMARINE"
... padded to 20 bytes would be:

"YELLOW SUBMARINE\x04\x04\x04\x04"
"""

# -*- coding: utf-8 -*-
__author__ = 'Lin'

# 以下参考了writeUp改的

import codecs

plaintext = "YELLOW SUBMARINE"
answer = b"YELLOW SUBMARINE\x04\x04\x04\x04"


def main():
    block_size = 20
    myanswer = pad(plaintext, block_size)
    assert (myanswer == answer)


def pad(plaintext, block_size=16):
    '''input: plaintext="abcdefg", block_size=10
       output: b"abcdefg\x03\x03\x03"'''
    padding_value = block_size - len(plaintext) % block_size
    output = codecs.encode(plaintext, "ascii") + bytes([padding_value]) * padding_value
    return output


if __name__ == "__main__":
    main()


