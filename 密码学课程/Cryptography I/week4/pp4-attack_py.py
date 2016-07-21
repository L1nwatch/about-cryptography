# 这是老师自己给的py文件

import urllib.request  # urllib.request在python3.x中被改为urllib.request
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='
# --------------------------------------------------------------
# padding oracle
# --------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib.request.quote(q)  # Create query URL
        req = urllib.request.Request(target)  # Send HTTP request to server
        try:
            f = urllib.request.urlopen(req)  # Wait for response
            print(f.getHeader())
        except urllib.request.HTTPError as e:
            print("We got: %d" % e.code)  # Print response code
            if e.code == 404:
                return True  # good padding
            return False  # bad padding


if __name__ == "__main__":
    po = PaddingOracle()
    quote = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
    po.query(quote)  # Issue HTTP query with the given argument



