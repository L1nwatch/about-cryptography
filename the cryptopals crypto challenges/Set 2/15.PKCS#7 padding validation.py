'''Write a function that takes a plaintext, determines if it has valid PKCS#7 padding, and strips the padding off.

The string:

"ICE ICE BABY\x04\x04\x04\x04"
... has valid padding, and produces the result "ICE ICE BABY".

The string:

"ICE ICE BABY\x05\x05\x05\x05"
... does not have valid padding, nor does:

"ICE ICE BABY\x01\x02\x03\x04"
If you are writing in a language with exceptions, like Python or Ruby, make your function throw an exception on bad padding.

Crypto nerds know where we're going with this. Bear with us.
====================================================================================================================
'''
# -*- coding: utf-8 -*-
__author__ = '__L1n__w@tch'

# 自己原先写的不太好，参考了write_up重写了一个

def main():
    padding_text = b"ICE ICE BABY\x04\x04\x04\x04"
    print(unpad_if_is_validation(padding_text))
    padding_text = b"ICE ICE BABY\x01\x02\x03\x04"
    print(unpad_if_is_validation(padding_text))
    padding_text = b"ICE ICE BABY\x05\x05\x05\x05"
    print(unpad_if_is_validation(padding_text))


'''
def unpad_if_is_validation(padding_text):
    """
    其实这里我有点疑惑，如果原文的最后一个是\x01这一类的要认为是合法还是不合法的?
    :param padding_text: b"ICE ICE BABY\x04\x04\x04\x04"
    :return: b"ICE ICE BABY"
    """
    padding_value = padding_text[-1]
    # 下面的这个-1错了，少了一个字节
    for each in padding_text[-(padding_value):-1]:
        if each != padding_value:
            raise ValueError
    return padding_text[:len(padding_text) - padding_value]
'''


def unpad_if_is_validation(padding_text, block_size=16):
    """
    :param padding_text: b"ICE ICE BABY\x04\x04\x04\x04"
    :return: b"ICE ICE BABY"
    """
    # 抛出异常也可以用assert
    assert ( len(padding_text) % block_size == 0)
    padding_value = padding_text[-1]
    # 以下的-1注意不要写成padding_text[-padding_value:-1]，这样导致少了一个字节
    assert ( padding_text[-padding_value:] == bytes([padding_value]) * padding_value)
    return padding_text[:len(padding_text) - padding_value]


if __name__ == "__main__":
    main()

