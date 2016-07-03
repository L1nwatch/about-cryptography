## 文件夹说明
这里存放的是之前参加第一节密码学复赛的比赛作品代码, 功能是实现通信双方各自产生 1024 bits 的 RSA 公钥(e=65537), 然后通过这个公钥交换得到 AES 密钥, 并用该 AES 密钥对文件进行加密并传送.

## PS
代码写的挺一般, 就当拿来学习 tkinter/RSA/AES 吧

## 代码运行截图
- ![服务端运行截图](https://github.com/L1nwatch/about-cryptography/blob/master/%E7%AC%AC%E4%B8%80%E5%B1%8A%E5%AF%86%E7%A0%81%E5%AD%A6%E5%A4%8D%E8%B5%9B/run_picture/server.png)
- ![客户端运行截图](https://github.com/L1nwatch/about-cryptography/blob/master/%E7%AC%AC%E4%B8%80%E5%B1%8A%E5%AF%86%E7%A0%81%E5%AD%A6%E5%A4%8D%E8%B5%9B/run_picture/client.png)
- ![成功通信截图](https://github.com/L1nwatch/about-cryptography/blob/master/%E7%AC%AC%E4%B8%80%E5%B1%8A%E5%AF%86%E7%A0%81%E5%AD%A6%E5%A4%8D%E8%B5%9B/run_picture/connect.png)

## 其他问题

### 打包成 exe 的问题

使用 Python3.5 打包老是报错，但是使用 Python3.4 + cx_freeze 却可以（需要自己手动复制tcl\tcl8.6）。

原因在于 os.envrion 里面没有 TCL_LIBRARY。

重装 Python3.5 一试。好吧，还是没有 TCL_LIBRARY。估计 Python3.5 有点问题吧，返回到 Python3.4.3 了。

### 手动解决方案：
    set TCL_LIBRARY=D:\Software\Python35\tcl\tcl8.6
    set TK_LIBRARY=D:\Software\Python35\tcl\tk8.6

    for windows
    in your dircetory "C:\Users\g2\Envs\DataVizproj\Scripts\activate.bat"
    just add
    set "TCL_LIBRARY=C:\Python27\tcl\tcl8.5"
    set "TK_LIBRARY=C:\Python27\tcl\tk8.5"
    and restart your cmd or shell
    worked
