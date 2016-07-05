"""
Should produce:

SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t

So go ahead and make that happen. You'll need to use this code for the rest of the exercises.
Cryptopals Rule

Always operate on raw bytes, never on encoded strings. Only use hex and base64 for pretty-printing.
"""

# 本来想自己实现hex2base64的（详看最下面注释）
# 不过发现还是用现有的库来解决好点
# 这道题还隐藏了一个：
# 对所给的16进制转成ascii码后得到：b"I'm killing your brain like a poisonous mushroom"
# 【PS】语句：codecs.decode(hex_string, 'hex')


import base64
import codecs


def main():
    test_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    right_answer = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    base64_text = hex2base64(test_string)
    print("right answer = {0}\nmy answer is {1}".format(right_answer, base64_text))


def hex2base64(hex_text):
    return base64.b64encode(codecs.decode(hex_text, "hex")) # 另一种写法bytes.fromhex(hex_text)也可以转为bytes


if __name__ == "__main__":
    main()

"""
如果要自己实现的话：
Base64编码要求把3个8位字节（3*8=24）转化为4个6位的字节（4*6=24）
之后在6位的前面补两个0，形成8位一个字节的形式。\

base64_map = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + \
             "abcdefghijklmnopqrstuvwxyz" + "0123456789+/="
"""


