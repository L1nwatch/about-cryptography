#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 题目描述
Write a k=v parsing routine, as if for a structured cookie. The routine should take:
    foo=bar&baz=qux&zap=zazzle
... and produce:
    {
      foo: 'bar',
      baz: 'qux',
      zap: 'zazzle'
    }
(you know, the object; I don't care if you convert it to JSON).
Now write a function that encodes a user profile in that format, given an email address. You should have something like:
    profile_for("foo@bar.com")
... and it should produce:
    {
      email: 'foo@bar.com',
      uid: 10,
      role: 'user'
    }
... encoded as:
    email=foo@bar.com&uid=10&role=user
Your "profile_for" function should not allow encoding metacharacters (& and =). Eat them, quote them,
whatever you want to do, but don't let people set their email address to "foo@bar.com&role=admin".
Now, two more easy functions. Generate a random AES key, then:
    Encrypt the encoded user profile under the key; "provide" that to the "attacker".
    Decrypt the encoded user profile and parse it.
Using only the user input to profile_for() (as an oracle to generate "valid" ciphertexts) and the ciphertexts themselves
, make a role=admin profile.

# 题意说明
现在有一个存在漏洞的程序, 该程序的功能是给定一个邮箱地址, 返回对应的格式化串, 同时可以进行加密, 解密, 解析格式化串的操作.
攻击者的目的就是构造一个邮箱, 得到对应的密文, 之后给被攻击的程序发送自己改过的密文(在不知道密钥的情况下), 使得攻击者的权限由 user 变成 admin
"""
import random
from Crypto.Cipher import AES

__author__ = '__L1n__w@tch'


def parsing_routine(data):
    """
    按规则进行解析操作
    :param data: 'foo=bar&baz=qux&zap=zazzle'
    :return: {'foo':'bar', 'baz':'qux', 'zap':'zazzle'}
    """
    dictionary = dict()
    for each_item in data.split('&'):
        [key, value] = each_item.split('=')  # 这里左边不用中括号也行
        dictionary.setdefault(key, value)

    return dictionary


def profile_for(email):
    """
    格式化操作, 将输入的邮箱按指定规则进行格式化
    :param email: b"foo@bar.com"
    :return: b"email=foo@bar.com&uid=10&role=user"
    """
    # 删掉邮箱中原有的 & 和 = 符号
    email.replace(b'&', b'')
    email.replace(b'=', b'')

    # 格式化操作
    output = list()
    output.append(b"email=" + email)
    output.append(b"uid=" + b"10")
    output.append(b"role=user")

    return b'&'.join(output)


def generate_random_bytes(size=16):
    """
    产生随机字节流
    :param size: 16
    :return: 随机字节流, 比如 b'\x01' * 3 + b"\x00" + b"\x14" * 12
    """
    return b"".join(random.sample([bytes([value]) for value in range(256)], size))


def aes_ecb_encrypt(data, secret_key):
    """
    进行 AES 加密操作, 会手动对 data 进行填充操作
    :param data: b"email=foo@bar.com&uid=10&role=user"
    :param secret_key: 所使用的密钥
    :return: b"ciphertext"
    """
    return AES.new(secret_key, AES.MODE_ECB).encrypt(pad(data))


def pad(data, block_size=16):
    """
    填充操作
    :param data: b'abc'
    :param block_size: 5
    :return: b'abc\x02\x02'
    """
    padding_value = block_size - len(data) % block_size
    return data + bytes([padding_value]) * padding_value


def aes_ecb_decrypt(data, secret_key):
    """
    进行 AES-ECB 解密操作, 会对解密后的结果进行填充解析
    :param data: b'ciphertext\x01'
    :param secret_key: 所使用的密钥
    :return: b'plaintext'
    """
    return unpad(AES.new(secret_key, AES.MODE_ECB).decrypt(data))


def unpad(padded_text, block_size=16):
    """
    填充解析, 将填充过后的数据还原为未填充的数据
    :param padded_text: b'aaa\x01'
    :param block_size: 4
    :return: b'aaa'
    """
    padding_value = padded_text[-1]
    return padded_text[:len(padded_text) - padding_value]


def attack():
    """
    进行攻击操作
    原文:
        |email=?&uid=10&role=user+pad|
    我们使得分块变成这种形式的即可:
        |email=?&uid=10&role=|admin|
    方法是通过控制?，然后把这个块顶替掉最后的user分区
        |email=10个字符|admin+pad|3个字符&uid=10&role=|user+pad|
    所以我们要构造的只有:
        10 个字符 + admin + 11 pad + 3 个字符
    :return: b'attack_ciphertext'
    """
    attack_email = b"Ineed@ten.admin" + b"\x0b" * 11 + b"com"
    return attack_email


if __name__ == "__main__":
    key = generate_random_bytes(16)
    # 演示正常的情况
    print("[*] {pad} 正常的情况 {pad}".format(pad="=" * 30))
    user_email = b"abcd@efg.com"
    after_profile = profile_for(user_email)
    after_parsing = parsing_routine(after_profile.decode("utf8"))
    after_encrypt = aes_ecb_encrypt(after_profile, key)
    after_decrypt = aes_ecb_decrypt(after_encrypt, key)
    after_decrypt_parsing = parsing_routine(after_decrypt.decode("utf8"))
    print("正常邮件: {}\n经过格式化后: {}\n对格式化后的结果进行解析: {}".format(user_email, after_profile, after_parsing))
    print("加密结果为: {}\n解密结果为: {}\n对解密后的结果进行解析: {}".format(after_encrypt, after_decrypt, after_decrypt_parsing))
    print("[*] {pad} 正常情况结束 {pad}".format(pad="=" * 30), end="\n\n")

    # 演示攻击
    print("[*] {pad} 演示攻击 {pad}".format(pad="=" * 30))
    attacker_email = attack()  # 攻击者控制的邮箱地址
    after_profile = profile_for(attacker_email)
    after_parsing = parsing_routine(after_profile.decode("utf8"))
    after_encrypt = aes_ecb_encrypt(after_profile, key)
    attacker_cipher_text = after_encrypt[:16] + after_encrypt[32:48] + after_encrypt[16:32]  # 攻击者控制的密文
    after_decrypt = aes_ecb_decrypt(attacker_cipher_text, key)
    after_decrypt_parsing = parsing_routine(after_decrypt.decode("utf8"))
    print("正常邮件: {}\n经过格式化后: {}\n对格式化后的结果进行解析: {}".format(attacker_email, after_profile, after_parsing))
    print("加密结果为: {}\n解密结果为: {}\n对解密后的结果进行解析: {}".format(after_encrypt, after_decrypt, after_decrypt_parsing))
    print("[*] {pad} 攻击结束 {pad}".format(pad="=" * 30))
