# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# url: http://cryptopals.com/sets/5/challenges/39/
# 题意: 手动实现RSA
# 步骤:
# 1.产生2个随机质数, p,q
# 2.n = p * q
# 3.et = (p - 1) * (q - 1)
# 4.e = 3
# 5.d = invmod(e, et)(exp, invmod(17,3120) = 2753)
# 6.PK = [E, N], SK = [D, N]
# 7.Encrypt: c=m ** e % n, Decrypt: m = c ** d % n
# 8.对代码进行测试（测试加密, 解密等）
# 9.十六进制表示

import gmpy2
import binascii
from Crypto.Util.number import getPrime


def main():
    rsa = MyRSA()
    rsa.show_keys()
    n, e, d = rsa.n, rsa.e, rsa.d
    test(rsa, n, e, d)


def test(rsa, n, e, d):
    # 由于所采用的p和q位数有限(512bits)，所以明文不宜过长（话说本来就不是用来加密长明文的）
    plaintext = b"Remember it need time to run!!!!!!"
    # 测试加密
    cipher_text = rsa.encrypt(binascii.hexlify(plaintext), e, n)
    # 测试解密
    result = binascii.unhexlify(hex(rsa.decrypt(cipher_text, d, n))[2:])
    print("Plain text is {0}\nCipher text is {1}\nDecrypt text is {2}".format(plaintext, cipher_text, result))


class MyRSA():
    def __init__(self):
        self.p, self.q, self.n, self.et, self.e, self.d = self.create_rsa()

    def create_rsa(self, e=3):
        while True:
            # 这里由于e固定为3, 而求d的时候invmod(3, et)不一定存在, 所以利用死循环直到生成合法数值
            try:
                p, q = self._generate_p_q()
                n = self._compute_n(p, q)
                et = self._compute_et(p, q)
                e = self._set_e(e)
                d = self._compute_d(e, et)

                return p, q, n, et, e, d
            except:
                pass

    def show_keys(self):
        print("P = {p}\nQ = {q}\nN = {n}\nET = {et}\nE = {e}\nD = {d}".format(
            p=self.p, q=self.q, n=self.n, et=self.et, e=self.e, d=self.d
        ))

    def encrypt(self, plaintext, e, n):
        message = gmpy2.mpz(plaintext, 16)
        return gmpy2.powmod(message, e, n)

    def decrypt(self, cipher_text, d, n):
        cipher_text = gmpy2.mpz(cipher_text)
        return gmpy2.powmod(cipher_text, d, n)

    def _generate_p_q(self, bit_length=512):
        # bit_length长度的p和q
        p = getPrime(bit_length)
        q = getPrime(bit_length)
        return p, q

    def _compute_n(self, p, q):
        return gmpy2.mpz(p) * gmpy2.mpz(q)

    def _compute_et(self, p, q):
        return gmpy2.mpz(p - 1) * gmpy2.mpz(q - 1)

    def _set_e(self, e=3):
        return e

    def _compute_d(self, e, et):
        return gmpy2.invert(e, et)


if __name__ == "__main__":
    main()

