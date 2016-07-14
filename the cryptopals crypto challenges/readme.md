# 网址
[the cryptopals crypto challenges](https://cryptopals.com/)

## 说明
此文件夹保存的是当时密码学实验时自己做的关于该网站的几个密码学挑战题, 采用的语言是 Python3

## 清单
* Crypto Challenge Set 1
    * 1. Convert hex to base64
        * 研究十六进制转换成 ascii 再转换成 base64 编码
    * 2. Fixed XOR
        * 实现 2 个十六进制串的异或
    * 3. Single-byte XOR cipher
        * 实现一个十六进制串与一个由单字符扩展而成的十六进制串异或
    * 4. Detect single-character XOR
        * 找出密文中被单字符加密的那一句密文, 并解密出来
        * 从解密结果中查找解密正确的英文句子(利用空格数量)
    * 5. Implement repeating-key XOR
        * 与第 3 题以及第 4 题类似, 不过不是单字符, 而是由一个字符串产生的十六进制串
    * 7. AES in ECB mode
        * 学习如何使用 AES-ECB 进行加密操作
    * 8. Detect AES in ECB mode
        * 找出被 AES-ECB 加密的密文
        * 利用的是一次密码本攻击(ECB 模式下对同样的明文加密总是产生相同的密文)
* Crypto Challenge Set 2
    * 9. Implement PKCS#7 padding
        * 实现 PKCS#7 填充操作
    * 10. Implement CBC mode
        * 要求不用密码库手动实现 AES-CBC(利用 AES-ECB )
    * 11. An ECB/CBC detection oracle
        * 随机选择 ECB 或者 CBC 模式进行加密，返回加密所采用的模式以及加密后的结果
        * 仅给定一段密文，判断是采用 ECB 模式还是使用 CBC 模式进行的加密
    * 13. ECB cut-and-paste
    * 14. Byte-at-a-time ECB decryption (Harder)
    * 15. PKCS#7 padding validation
* Crypto Challenge Set 3
    * 17. The CBC padding oracle
    * 18. Implement CTR, the stream cipher mode
    * 22. Crack an MT19937 seed
    * 23. Clone an MT19937 RNG from its output
    * 24. Create the MT19937 stream cipher and break it
* Crypto Challenge Set 4
    * 27. Recover the key from CBC with IV=Key
* Crypto Challenge Set 5
    * 39. Implement RSA
        * 手动实现RSA, 包括加密和解密等操作
    * 40. Implement an E=3 RSA Broadcast attack
* Crypto Challenge Set 6
    * 41. Implement unpadded message recovery oracle
    * 46. RSA parity oracle
