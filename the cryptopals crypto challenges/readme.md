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
        * 随机选择 ECB 或者 CBC 模式进行加密, 返回加密所采用的模式以及加密后的结果
        * 仅给定一段密文, 判断是采用 ECB 模式还是使用 CBC 模式进行的加密
    * 13. ECB cut-and-paste
        * 现在有一个存在漏洞的程序, 该程序的功能是给定一个邮箱地址, 返回对应的格式化串, 同时可以进行加密, 解密, 解析格式化串的操作.
        * 攻击者的目的就是构造一个邮箱, 得到对应的密文, 之后给被攻击的程序发送自己改过的密文(在不知道密钥的情况下), 使得攻击者的权限由 user 变成 admin
        * 利用 AES-ECB 的填充进行攻击
    * 14. Byte-at-a-time ECB decryption (Harder)
        * 一个字节一个字节地对特定明文格式的 ECB 加密结果进行破解操作
    * 15. PKCS#7 padding validation
        * 实现一下 PKCS#7 解填充, 如果格式不合法需要抛出异常
* Crypto Challenge Set 3
    * 17. The CBC padding oracle
        * 利用 CBC 填充进行攻击, 即只要服务器可能返回一个密文是否合法（通过填充值判断）, 就有机会让攻击者还原出明文
        * 原理主要是异或两次相当于没有异或, 攻击者接着利用 CBC 模式的特点尝试爆破
    * 18. Implement CTR, the stream cipher mode
        * 利用 ECB 手动实现 CTR 模式的解密操作, 解密题目中给定的密文
    * 22. Crack an MT19937 seed
        * 证明只要知道 MT19937(随机数生成器)的一个输出值, 可以根据这个输出值找到随机数生成器所采用的种子
        * 原理是爆破可能的种子, 判断生成的随机数是否一致, 就可以知道这个是不是种子了
    * 23. Clone an MT19937 RNG from its output
        * 实现一个 MT19937 随机数生成器的复制操作
        * 仅需知道 MT19937 产生的 624 个值就可以完成这个复制操作, 无需知道种子, 也无需爆破种子
        * 原理是 MT19937 算法中的 temper 操作存在逆算法, 实现该逆算法再利用 624 个值就可以实现克隆了
    * 24. Create the MT19937 stream cipher and break it
        * 利用 MT19937 实现流加密算法
        * 给定一个密文, 已知该密文的部分明文, 比如说明文后缀, 破解该密文
        * 利用的原理是异或两次相当于没有异或, 另一个原理是爆破种子, 参考 Challenge 22
        * 顺带实现一个实例(密码令牌), 该 token 以时间戳作为种子, 攻击者可以爆破得到对应的密码令牌
* Crypto Challenge Set 4
    * 27. Recover the key from CBC with IV=Key
* Crypto Challenge Set 5
    * 39. Implement RSA
        * 手动实现RSA, 包括加密和解密等操作
    * 40. Implement an E=3 RSA Broadcast attack
* Crypto Challenge Set 6
    * 41. Implement unpadded message recovery oracle
    * 46. RSA parity oracle
