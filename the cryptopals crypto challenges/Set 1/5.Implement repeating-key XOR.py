"""
 Here is the opening stanza of an important work of the English language:

Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal

Encrypt it, under the key "ICE", using repeating-key XOR.

In repeating-key XOR, you'll sequentially apply each byte of the key; the first byte of plaintext will be XOR'd against I, the next C, the next E, then I again for the 4th byte, and so on.

It should come out to:

0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f

Encrypt a bunch of stuff using your repeating-key XOR function. Encrypt your mail. Encrypt your password file. Your .sig file. Get a feel for it. I promise, we aren't wasting your time with this.
"""

# -*- coding: utf-8 -*-
__author__ = 'Lin'

# url: http://cryptopals.com/sets/1/challenges/5/
# 题意: 将KEY"ICE"与明文异或即可
# 这道题的plaintext得自己手动加个\n啊，要不然中间还会有问题。。（不能直接回车换行，windos下会变成\r\n的）


def main():
    # 字符串过长了
    answer = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a2622632427276527" \
             "2a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    plaintext = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = "ICE"

    my_answer = xor(plaintext, key)
    print(my_answer)
    print(answer)
    assert (my_answer == answer)


def xor(plaintext, key):
    """
    :param plaintext: "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    :param key: "ICE"
    :return: "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    """
    plaintext = bytes(plaintext, "ascii")
    key = bytes(key, "ascii")
    answer = ''
    for i in range(len(plaintext)):
        # zfill是为了保证0xb的时候能表示为0x0b
        answer += hex(plaintext[i] ^ key[i % len(key)])[2:].zfill(2)

    return answer


if __name__ == '__main__':
    main()

"""
==================================================================================================================
网上WriteUp
def mc_part5():

      def cycle_key(key):
        idx = 0
        while True:
          yield ord(key[idx%len(key)]) # 带有 yield 的函数在 Python 中被称之为 generator（生成器）
          idx += 1

      g = cycle_key('ICE')
      s = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
      hh = bytes(s,'ascii')
      xored = bytes([a^b for (a,b) in zip(hh, g)])

      c = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
      expected = bytes.fromhex(c)
      assert( xored == expected )
"""