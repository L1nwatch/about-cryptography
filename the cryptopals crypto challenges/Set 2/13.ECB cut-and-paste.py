'''
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
Your "profile_for" function should not allow encoding metacharacters (& and =). Eat them, quote them, whatever you want to do, but don't let people set their email address to "foo@bar.com&role=admin".

Now, two more easy functions. Generate a random AES key, then:

Encrypt the encoded user profile under the key; "provide" that to the "attacker".
Decrypt the encoded user profile and parse it.
Using only the user input to profile_for() (as an oracle to generate "valid" ciphertexts) and the ciphertexts themselves, make a role=admin profile.
====================================================================================================================
'''
# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# 发现最近的题真是完全不知道它想干嘛，总之一步一步来
# 一开始全部用字节来表示，不过最后还是觉得用字符好点,主要是10那里的处理
# 但是加密解密的时候传输的数据就都要用字节形式了

import random
from Crypto.Cipher import AES


def main():
    global key
    key = prf(16)
    ciphertext = attack()  # 我们能控制的只有密文
    plaintext = parsing_routine(decrypt(ciphertext).decode("utf-8"))
    print(plaintext)  # 目标是就是使得plaintext能够输出role:admin的字样


def parsing_routine(data):
    """
    :param data: 'foo=bar&baz=qux&zap=zazzle'
    :return: {'foo':'bar', 'baz':'qux', 'zap':'zazzle'}
    """
    dictionary = dict()
    for each in data.split('&'):
        [key, value] = each.split('=')  # 这里左边不用中括号也行
        dictionary.setdefault(key, value)

    return dictionary


def profile_for(email):
    """
    this function will eat & or =
    :param email: "foo@bar.com"
    :return: "email=foo@bar.com&uid=10&role=user"
    """
    email.replace('&', '')
    email.replace('=', '')

    output = list()
    output.append("email" + '=' + email)
    output.append("uid" + '=' + str(10))
    output.append("role" + '=' + "user")

    return '&'.join(output)


def prf(size=16):
    """
    :param size: 16
    :return: such as b'\x01' * 16
    """
    return b"".join(random.sample([bytes([value]) for value in range(256)], size))


def encrypt(plaintext):
    """
    :param plaintext: b"email=foo@bar.com&uid=10&role=user"
    :return: b"ciphertext"
    """
    encryptor = AES.new(key, AES.MODE_ECB)
    return encryptor.encrypt(pad(plaintext))


def pad(plaintext, block_size=16):
    """
    :param plaintext: b'abc'
    :param block_size: 5
    :return: b'abc\x02\x02'
    """
    padding_value = block_size - len(plaintext) % block_size
    return plaintext + bytes([padding_value]) * padding_value


def decrypt(ciphertext):
    """
    :param ciphertext: b'ciphertext\x01'
    :return: b'plaintext'
    """
    decryptor = AES.new(key, AES.MODE_ECB)
    plaintext = decryptor.decrypt(ciphertext)
    return unpad(plaintext)


def unpad(plaintext, block_size=16):
    """
    :param plaintext: b'aaa\x01'
    :param block_size: 4
    :return: b'aaa'
    """
    padding_value = plaintext[-1]
    return plaintext[:len(plaintext) - padding_value]


def attack():
    """
    |email=?&uid=10&role=user+pad|
    我们使得分块变成这种形式的即可:
    |email=?&uid=10&role=|admin|
    方法是通过控制?，然后把这个块顶替掉最后的user分区
    |email=10个字符|admin+pad|3个字符&uid=10&role=|user+pad|
    所以我们要构造的只有:10个字符+admin+11pad+3个字符
    :return: b'attack_ciphertext'
    """
    attack_email = b"Ineed@ten.admin" + b"\x0b" * 11 + b"com"
    attack_profile = b"email=" + attack_email + b"&uid=10&role=user"
    ciphertext = encrypt(attack_profile)
    attack_ciphertext = ciphertext[:16] + ciphertext[32:48] + ciphertext[16:32]
    return attack_ciphertext


if __name__ == "__main__":
    main()

