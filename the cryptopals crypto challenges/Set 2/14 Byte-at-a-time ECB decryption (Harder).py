# -*- coding: utf-8 -*-
# version: Python3.X
__author__ = '__L1n__w@tch'

# url: http://cryptopals.com/sets/2/challenges/14/
# 题意: 在chall12的基础上更改了一下加密的明文, 原先加密的明文是
# AES-128-ECB(your-string || unknown-string, random-key)
# 现在加上随机字符前缀: AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)
# 目标跟chall12一样, 破解出明文

import os
import base64
from Crypto.Cipher import AES
from itertools import zip_longest

# 随机前缀
prefix = None
random_key = os.urandom(16)


def main():
    global prefix
    prefix = generate_random_prefix()

    over_length, block_order = detect_prefix_length()
    plaintext_length = detect_plaintext_length(over_length, block_order)

    # 爆破明文了, 原理跟chall12一样, 一个字节一个字节地探测
    plaintext = crack_plaintext(plaintext_length, over_length, block_order)
    print(plaintext)


def crack_plaintext(plaintext_length, over_length, block_order):
    plaintext = b""
    for i in range(plaintext_length):
        # 从最后一个字节开始爆破, 原理参考chall12
        padLen = over_length + 15 - (len(plaintext) % 16)
        pad = b"A" * padLen
        attack_pad_cipher_text = encrypt(pad)

        # 待爆破的节区
        attack_block_order = block_order + (len(plaintext) // 16)
        cipher_blocks = divide_group(attack_pad_cipher_text, 16)
        attack_block = cipher_blocks[attack_block_order]

        # 该节区的前缀
        new_prefix = (pad + plaintext)[-15:]
        # 获取该节区的最后一个未知字节
        plaintext += get_last_byte(new_prefix, attack_block, over_length, block_order)

    return plaintext


def get_last_byte(prefix, attack_block, over_length, block_order):
    # 只留最后一个字节来遍历
    plain = b"A" * (over_length + 15 - len(prefix))
    plain += prefix

    # 遍历最后一个字节的每一个可能值
    for i in range(256):
        attack_plaintext = plain + bytes(chr(i), "ascii")
        if (divide_group(encrypt(attack_plaintext), 16)[block_order] == attack_block):
            return bytes(chr(i), "ascii")

    raise Exception("爆破失败！")


def encrypt(attacker_controlled_plaintext):
    global prefix
    global random_key
    padding_string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg" \
                     "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq" \
                     "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg" \
                     "YnkK"

    plaintext = prefix + attacker_controlled_plaintext + base64.b64decode(padding_string)

    cipher_text = AES.new(random_key, AES.MODE_ECB).encrypt(pad(plaintext))
    return cipher_text


def detect_prefix_length():
    # 探测所用的前缀的长度
    # 注意ECB加密的特点，如果2个块的明文完全相同, 那么其加密结果也是相同的
    # 返回值有2个, 一个是prefix超出block_size的长度,为了后面计算明文长度用
    # 另一个是首次出现的能被控制的块的序号(顺带可以由此推出prefix的长度)
    for length in range(256):
        attack_plaintext = b"A" * length
        cipher = encrypt(attack_plaintext)
        cipherBlocks = divide_group(cipher, 16)
        for i in range(len(cipherBlocks) - 1):
            if (cipherBlocks[i] == cipherBlocks[i + 1]):
                over_length = len(attack_plaintext) % 16
                block_order = i
                return over_length, block_order


def generate_random_prefix():
    # 随机产生随机长度的随机串
    prefix = b""
    for i in range(int.from_bytes(os.urandom(1), "big")):
        prefix += os.urandom(1)

    return prefix


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


def pad(plaintext, size=16):
    """input: plaintext=b"abcdefg", block_size=10
       output: b"abcdefg\x03\x03\x03"."""
    padding_value = size - len(plaintext) % size
    output = plaintext + bytes([padding_value]) * padding_value
    return output


def detect_plaintext_length(over_length, block_order):
    # 我们令attacker-controlled为空, 这样我们加密的明文就是random-prefix || target-bytes
    # 于是我们就可以推导出target-bytes的长度, 算法如下:
    attack_plaintext = b""
    empty_control_length = len(encrypt(b""));
    # 做chall12时已知的条件, 题目故意给出1个字节的长度让我们重现攻击, 这里明文最大的长度即为prefix长度为0的情况
    max_plaintext_length = empty_control_length - 1

    # 一个字节一个字节地填充
    while (True):
        attack_plaintext += b'A'
        if (len(encrypt(attack_plaintext)) == empty_control_length):
            # 说明是填充值(因为是填充值所以长度才会一样, 填充值就是为了保持16的倍数)
            max_plaintext_length -= 1
        else:
            return max_plaintext_length + over_length - (block_order * 16)


if __name__ == "__main__":
    main()


