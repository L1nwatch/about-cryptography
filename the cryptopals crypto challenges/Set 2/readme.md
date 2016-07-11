# 网上关于第 10 题的 writeup
```Python
def mc_part10():
    raw = crypto_utils.b64_file_to_bytes('p10.txt')  # 没找到这个库，估计是自己自定义的吧
    iv = b'\x00' * 16  # initialisation vector - zero'ed
    key = b'YELLOW SUBMARINE'
    print(crypto_utils.aes_manual_cbc(key, raw, iv, mode=crypto_utils.MODE_DECRYPT))


def aes_manual_cbc(k, txt, iv, mode=MODE_DECRYPT):
    assert (isinstance(k, bytes))  # 用这个方法来判断输入的类型，可以参考一下
    assert (isinstance(txt, bytes))
    assert (isinstance(iv, bytes))
    assert (len(iv) == 16)

    from Crypto.Cipher import AES  # 这居然写在函数里面了，合适么。。。
    cr = AES.new(k, AES.MODE_ECB)
    prev_block = iv
    d = bytearray()
    for block in get_blocks(txt, size=16):
        if mode == MODE_ENCRYPT:
            prev_block = cr.encrypt(xor_bytearrays(prev_block, block))
            d.extend(prev_block)  # extend函数，其实就是+=吧？ extend()		——		扩展列表（用另一个列表）
        else:
            d.extend(xor_bytearrays(cr.decrypt(block), prev_block))
            prev_block = block

    return unpad(d)
```