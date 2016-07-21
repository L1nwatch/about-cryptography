# -*- coding: utf-8 -*-
__author__ = 'Lin'

import hashlib


h = ''
blocks = []
data = 'foo'

with open('/tmp/video_known.mp4', 'rb') as f:
    while data != '':
        data = f.read(1024)
        if data != '':
            blocks.insert(0, data)

for data in blocks:
        h = hashlib.sha256(data + h).digest()

assert h.encode('hex') == '03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8'


h = ''
blocks = []
data = 'foo'

with open('/tmp/video_unknown.mp4', 'rb') as f:
    while data != '':
        data = f.read(1024)
        if data != '':
            blocks.insert(0, data)

for data in blocks:
        h = hashlib.sha256(data + h).digest()

print(h.encode('hex'))

