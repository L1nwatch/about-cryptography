#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
Take your oracle function from #12. Now generate a random count of random bytes and prepend this string to every
plaintext. You are now doing:
    AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)
Same goal: decrypt the target-bytes.
Stop and think for a second.
What's harder than challenge #12 about doing this? How would you overcome that obstacle?
The hint is: you're using all the tools you already have; no crazy math is required.

Think "STIMULUS" and "RESPONSE".
# 题意
在 challenge12 的基础上更改了一下加密的明文, 原先加密的明文是
    AES-128-ECB(your-string || unknown-string, random-key)
现在加上随机字符前缀:
    AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)

目标跟 challenge12 一样, 破解出明加密字段中的 target_bytes 字段
"""
import os
import base64
from Crypto.Cipher import AES
from itertools import zip_longest

__author__ = '__L1n__w@tch'


class MyCrypto:
    def __init__(self):
        self.random_key = os.urandom(16)  # 产生固定长度为 16 的随机字节流
        self.prefix = generate_random_bytes()  # 产生随机长度(0~255)的随机字节流
        base64_encoded = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg" \
                         "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq" \
                         "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg" \
                         "YnkK"
        self.target_plaintext = base64.b64decode(base64_encoded)

    def encrypt(self, attacker_controlled_plaintext):
        """
        进行加密操作, 按照指定的格式:
            AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)
        :param attacker_controlled_plaintext: 攻击者能控制的那一部分待加密字段
        :return: 加密过后的结果
        """
        data = self.prefix + attacker_controlled_plaintext + self.target_plaintext

        cipher_text = AES.new(self.random_key, AES.MODE_ECB).encrypt(self.pad(data))
        return cipher_text

    @classmethod
    def pad(cls, data, size=16):
        """
        进行填充操作
        :param data: b"abcdefg", 待填充字节流
        :param size: 10, 要填充至多长
        :return: b"abcdefg\x03\x03\x03"
        """
        padding_value = size - len(data) % size
        output = data + bytes([padding_value]) * padding_value
        return output


def crack_plaintext(normal_program, length, over_length, block_order):
    """
    尝试爆破待破解的目标字段
    :param normal_program: 待破解的程序, 提供加密等功能
    :param length: 待破解明文的长度
    :param over_length: prefix 超出 block_size 的长度
    :param block_order: 首个可控的 block 序号
    :return: 尝试破解得到的目标字段
    """
    result = bytes()

    # 一个字节一个字节爆破目标字段
    for i in range(length):
        # 从最后一个字节开始爆破, 原理参考 challenge12
        padding_length = over_length + 15 - (len(result) % 16)
        pad = b"A" * padding_length
        attack_pad_cipher_text = normal_program.encrypt(pad)

        # 待爆破的节区
        attack_block_order = block_order + (len(result) // 16)
        cipher_blocks = divide_group(attack_pad_cipher_text, 16)
        attack_block = cipher_blocks[attack_block_order]

        # 该节区的前缀
        new_prefix = (pad + result)[-15:]

        # 获取该节区的最后一个未知字节
        result += get_last_byte(normal_program, new_prefix, attack_block, over_length, block_order)

    return result


def get_last_byte(normal_program, prefix, attack_block, over_length, block_order):
    """
    获取某一节中最后一个字节
    :param normal_program: 待攻击的程序
    :param prefix: 自己模拟的前缀
    :param attack_block: 要攻击第几块
    :param over_length: prefix 超出 block_size 的长度
    :param block_order: 首个可控的块序号
    :return: 破解得到的字节
    """
    # 只留最后一个字节来遍历
    plain = b"A" * (over_length + 15 - len(prefix))
    plain += prefix

    # 遍历最后一个字节的每一个可能值
    for i in range(256):
        attack_plaintext = plain + bytes(chr(i), "ascii")
        if divide_group(normal_program.encrypt(attack_plaintext), 16)[block_order] == attack_block:
            return bytes(chr(i), "ascii")

    raise Exception("爆破失败！")


def detect_prefix_length(normal_program):
    """
    探测程序加密时所用的前缀的长度
    注意 ECB 加密的特点，如果 2 个块的明文完全相同, 那么其加密结果也是相同的
    返回值有2个, 一个是 prefix 超出 block_size 的长度,为了后面计算明文长度用
    另一个是首次出现的能被控制的块的序号(顺带可以由此推出prefix的长度)
    :param normal_program: 待攻击的程序, 此程序能提供加密等功能
    :return: such as (15, 10)
    """
    length = int()  # prefix 超出 block_size 的长度
    order = int()  # 能被控制的块的序号

    for length in range(256):
        attack_plaintext = b"A" * length
        cipher_text = normal_program.encrypt(attack_plaintext)  # 使用程序的加密功能进行加密
        cipher_blocks = divide_group(cipher_text, 16)  # 按 16 字节进行分组操作

        # 探测前缀长度, 原理是利用 ECB 加密的特点(一次密码本)
        for i in range(len(cipher_blocks) - 1):
            if cipher_blocks[i] == cipher_blocks[i + 1]:
                length = len(attack_plaintext) % 16
                order = i
                break

    return length, order


def generate_random_bytes():
    """
    产生随机长度的随机字节串
    :return: b'\xfe\xbb%]@\xa0(\xa8k\xcd\x19\x05m\x04\xcaa'
    """
    bytes_text = bytes()
    for i in range(int.from_bytes(os.urandom(1), "big")):
        bytes_text += os.urandom(1)

    return bytes_text


def divide_group(data, size):
    """
    进行分组操作
    :param data: b"abcdefghi"
    :param size: 3
    :return: [b"abc", b"def", b"ghi"]
    """
    args = [iter(data)] * size

    blocks = []
    for block in zip_longest(*args):
        blocks.append(b"".join([bytes([value]) for value in block]))

    return blocks


def detect_plaintext_length(normal_program, over_length, block_order):
    """
    探测待破解字段的长度, 注意加密格式为:
        AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)

    我们令 attacker-controlled 为空, 这样我们加密的明文就是
        random-prefix || target-bytes
    于是我们就可以推导出 target-bytes 的长度
    :param normal_program: 待攻击的程序, 包含加密等功能
    :param over_length: prefix 超出 block_size 的长度, such as 15
    :param block_order: 首个可控的块的序号, such as 10
    :return: 待破解明文的长度, such as 10
    """
    attack_plaintext = bytes()

    # 令 attacker-controlled 为空, 看加密后的长度为多少
    empty_control_length = len(normal_program.encrypt(attack_plaintext))

    # 做 challenge12 时已知的条件, 题目故意给出 1 个字节的长度让我们重现攻击, 这里明文最大的长度即为 prefix 长度为 0 的情况
    max_plaintext_length = empty_control_length - 1

    # 一个字节一个字节地填充
    while True:
        attack_plaintext += b'A'
        if len(normal_program.encrypt(attack_plaintext)) == empty_control_length:
            # 说明是填充值(因为是填充值所以长度才会一样, 填充值就是为了保持16的倍数)
            max_plaintext_length -= 1
        else:
            return max_plaintext_length + over_length - (block_order * 16)


if __name__ == "__main__":
    wait_to_attack = MyCrypto()  # 待攻击的代码

    # 攻击第一步, 探测前缀
    prefix_overstep_length, under_control_block_order = detect_prefix_length(wait_to_attack)

    # 攻击第二步, 探测待破解明文长度
    plaintext_length = detect_plaintext_length(wait_to_attack, prefix_overstep_length, under_control_block_order)

    # 攻击第三步, 爆破明文了, 原理跟 challenge12 一样, 一个字节一个字节地探测
    after_crack = crack_plaintext(wait_to_attack, plaintext_length, prefix_overstep_length, under_control_block_order)

    print(after_crack)
