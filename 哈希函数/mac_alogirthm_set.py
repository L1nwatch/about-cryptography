#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 各种哈希函数的集合
"""
from hashlib import md5
from Crypto.Hash import MD5

from hashlib import sha1
from Crypto.Hash import SHA

from hashlib import sha224
from Crypto.Hash import SHA224

from hashlib import sha256
from Crypto.Hash import SHA256

from hashlib import sha384
from Crypto.Hash import SHA384

from hashlib import sha512
from Crypto.Hash import SHA512

import zlib

__author__ = '__L1n__w@tch'


class Hash:
    @staticmethod
    def hashlib_md5(data):
        """
        调用 hashlib 库的 md5 函数进行哈希操作
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "3d07f2120499e7bc692a492120f8be9b"
        """
        return md5(data).hexdigest()

    @staticmethod
    def crypto_hash_md5(data):
        """
        调用 Crypto 库的 md5 进行哈希操作
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "3d07f2120499e7bc692a492120f8be9b"
        """
        return MD5.new(data).hexdigest()

    @staticmethod
    def hashlib_sha1(data):
        """
        调用 hashlib 库的 sha1 函数进行哈希操作
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "327d106bf608b1f63bf5cbc5d1b6ea2d6836b446"
        """
        return sha1(data).hexdigest()

    @staticmethod
    def crypto_hash_sha1(data):
        """
        调用 Crypto 库的 sha1 函数进行哈希操作
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "327d106bf608b1f63bf5cbc5d1b6ea2d6836b446"
        """
        return SHA.new(data).hexdigest()

    @staticmethod
    def hashlib_sha224(data):
        """
        调用 hashlib 库的 sha224 函数进行哈希操作
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "acbcc08b23f746664cb9ce1ff6f234a76311d94a0c64108abc4c290f"
        """
        return sha224(data).hexdigest()

    @staticmethod
    def crypto_hash_sha224(data):
        """
        调用 Crypto 库的 sha224 函数进行哈希操作
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "acbcc08b23f746664cb9ce1ff6f234a76311d94a0c64108abc4c290f"
        """
        return SHA224.new(data).hexdigest()

    @staticmethod
    def hashlib_sha256(data):
        """
        调用 hashlib 库的 sha256 函数进行哈希操作
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "6b70a820eb978882fa49b199c853a5676e5e1a4744371be5affd4b3af1f5dde6"
        """
        return sha256(data).hexdigest()

    @staticmethod
    def crypto_hash_sha256(data):
        """
        调用 Crypto 库的 sha256 函数进行哈希操作
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "6b70a820eb978882fa49b199c853a5676e5e1a4744371be5affd4b3af1f5dde6"
        """
        return SHA256.new(data).hexdigest()

    @staticmethod
    def hashlib_sha384(data):
        """
        调用 hashlib 库的 sha384 函数进行哈希操作
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "708af8efbb882bb662a5a5f19d3164133621266903cec7ee0ce9eca950a7b7f8d09defedb4474da4257274741f2a07a8"
        """
        return sha384(data).hexdigest()

    @staticmethod
    def crypto_hash_sha384(data):
        """
        调用 Crypto 库的 sha384 函数进行哈希操作
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "708af8efbb882bb662a5a5f19d3164133621266903cec7ee0ce9eca950a7b7f8d09defedb4474da4257274741f2a07a8"
        """
        return SHA384.new(data).hexdigest()

    @staticmethod
    def hashlib_sha512(data):
        """
        调用 hashlib 库的 sha512 函数进行哈希操作
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "5a32f0967623012cdd4c29257f808f3f209184e992c39dc6d931f89831e7b1eb9379f9e3a20da09eb06d0ca53bd9c0845dda91baed17a713c0cac8a24259c0b9"
        """
        return sha512(data).hexdigest()

    @staticmethod
    def crypto_hash_sha512(data):
        """
        调用 Crypto 库的 sha512 函数进行哈希操作
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "5a32f0967623012cdd4c29257f808f3f209184e992c39dc6d931f89831e7b1eb9379f9e3a20da09eb06d0ca53bd9c0845dda91baed17a713c0cac8a24259c0b9"
        """
        return SHA512.new(data).hexdigest()

    @staticmethod
    def zlib_crc32(data):
        """
        调用 zlib 库的 crc32 函数算出校验值
        :param data: 待哈希的数值, 比如 b"test_hash"
        :return: "d4c14877"
        """
        return hex(zlib.crc32(data))[2:]


def hash_update():
    """
    讨论一下哈希库提供的 update 函数, 第一次使用结果跟直接哈希是一样的, 但是第二次使用 update 就不是直接哈希的结果了
    :return: None
    """
    text = b'aa'
    new_text = b'cc'

    hash_256 = SHA256.new()
    hash_256.update(text)
    print("first hash:{0}".format(hash_256.digest()))
    hash_256.update(new_text)
    print("Second hash:{0}".format(hash_256.digest()))

    print("first hash:{0}".format(SHA256.new(text).digest()))
    print("Second hash:{0}".format(SHA256.new(new_text).digest()))


if __name__ == "__main__":
    pass
