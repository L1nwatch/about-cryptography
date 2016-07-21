# -*- coding: utf-8 -*-
__author__ = 'Lin'

import urllib.request
import re
import codecs

# 获取网页状态码参考http://www.jb51.net/article/57039.htm
# HTTPResponse类在http.client中，可用help(http.client.HTTPResponse)查询帮助

def get_proxy_iplist(proxy_url):
    """实现功能：到代理网站上获取代理服务器的IP地址和端口"""
    # proxy_url = "http://cn-proxy.com/archives/218"
    response = urllib.request.urlopen(proxy_url)
    html = codecs.decode(response.read(), "utf-8")

    re_result = re.findall(r"<td>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}</td>\n<td>\d{1,5}</td>", html)

    proxy_iplist = []
    for each in re_result:
        # .匹配除换行符以外的，+匹配0~无穷多次
        [ip_address, port] = re.findall(r"<td>.+</td>", each)
        ip_address = ip_address[len("<td>"):-len("<len>")]
        port = port[len("<td>"):-len("<len>")]

        proxy_iplist.append(str(ip_address) + ':' + str(port))

    return proxy_iplist


def main():
    pass


if __name__ == "__main__":
    main()
    # get_proxy_iplist("http://www.kuaidaili.com/free/outha/")

