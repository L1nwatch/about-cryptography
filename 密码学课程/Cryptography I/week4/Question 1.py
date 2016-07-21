# -*- coding: utf-8 -*-
__author__ = 'Lin'

import codecs


def main():
    hex_string = "20814804c1767293b99f1d9cab3bc3e7"
    pos = 8
    bin_string = codecs.decode(hex_string, "hex")
    val = codecs.decode(hex(bin_string[pos] ^ ord('1') ^ ord('5'))[2:].zfill(2), "hex")
    bin_string = bin_string[0:pos] + val + bin_string[pos + 1:]
    print(bin_string)
    ans = ""
    for each_byte in bin_string:
        ans += hex(each_byte)[2:].zfill(2)

    print(ans)


if __name__ == "__main__":
    main()

