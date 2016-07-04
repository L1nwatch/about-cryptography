#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试哈希算法结果的正确性
"""
import unittest
from mac_alogirthm_set import Hash

__author__ = '__L1n__w@tch'


class TestMac(unittest.TestCase):
    """
    测试哈希的类
    """

    def setUp(self):
        self.test_text = b"test_hash"
        self.md5_answer = "3d07f2120499e7bc692a492120f8be9b"
        self.sha512_answer = "5a32f0967623012cdd4c29257f808f3f209184e992c39dc6d931f89831e7b1eb9379f9e3a20da09eb06d0ca53bd9c0845dda91baed17a713c0cac8a24259c0b9"
        self.sha384_answer = "708af8efbb882bb662a5a5f19d3164133621266903cec7ee0ce9eca950a7b7f8d09defedb4474da4257274741f2a07a8"
        self.sha256_answer = "6b70a820eb978882fa49b199c853a5676e5e1a4744371be5affd4b3af1f5dde6"
        self.sha224_answer = "acbcc08b23f746664cb9ce1ff6f234a76311d94a0c64108abc4c290f"
        self.sha1_answer = "327d106bf608b1f63bf5cbc5d1b6ea2d6836b446"
        self.crc32_answer = "d4c14877"

    def test_md5(self):
        self.failUnless(Hash.hashlib_md5(self.test_text) == self.md5_answer)
        self.failUnless(Hash.crypto_hash_md5(self.test_text) == self.md5_answer)

    def test_sha1(self):
        self.failUnless(Hash.hashlib_sha1(self.test_text) == self.sha1_answer)
        self.failUnless(Hash.crypto_hash_sha1(self.test_text) == self.sha1_answer)

    def test_sha224(self):
        self.failUnless(Hash.hashlib_sha224(self.test_text) == self.sha224_answer)
        self.failUnless(Hash.crypto_hash_sha224(self.test_text) == self.sha224_answer)

    def test_sha256(self):
        self.failUnless(Hash.hashlib_sha256(self.test_text) == self.sha256_answer)
        self.failUnless(Hash.crypto_hash_sha256(self.test_text) == self.sha256_answer)

    def test_sha384(self):
        self.failUnless(Hash.hashlib_sha384(self.test_text) == self.sha384_answer)
        self.failUnless(Hash.crypto_hash_sha384(self.test_text) == self.sha384_answer)

    def test_sha512(self):
        self.failUnless(Hash.hashlib_sha512(self.test_text) == self.sha512_answer)
        self.failUnless(Hash.crypto_hash_sha512(self.test_text) == self.sha512_answer)

    def test_crc32(self):
        self.failUnless(Hash.zlib_crc32(self.test_text) == self.crc32_answer)


if __name__ == "__main__":
    unittest.main()
    exit()

    # 需要单独测试的时候才使用下边这些
    suite = unittest.TestSuite()
    suite.addTest(TestMac("test_md5"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
