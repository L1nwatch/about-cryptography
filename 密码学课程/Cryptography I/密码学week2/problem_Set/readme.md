## 字典排序问题
```Python
sorted(iterable[, cmp[, key[, reverse]]]）
```

（1）iterable：是可迭代类型类型;

（2）cmp：用于比较的函数，比较什么由key决定,有默认值，迭代集合中的一项;

（3）key：用列表元素的某个属性和函数进行作为关键字，有默认值，迭代集合中的一项;

（4）reverse：排序规则. reverse = True 或者 reverse = False，有默认值，默认为升序排列（False）

【以下是第一题的代码】
【PS：
由于dictionary.items()返回的是一个元组，所以用key+lambda表示用值来排序（即选中返回的元组的第二个元素）】
```Python
__author__ = 'Lin'

dictionary = {}
dictionary['1'] = 1 / (2 ** 128)
dictionary['2'] = 1 / (10 ** 6)
dictionary['3'] = (1 / (10 ** 6)) ** 5
dictionary['4'] = (1 / (10 ** 6)) ** 6
dictionary['5'] = (1 / (10 ** 6)) ** 7

print(sorted(dictionary.items(), key =lambda x:x[1], reverse = True))
```

## 时间
```Python
# import datetime # 本来想用datetime库的，结果发现这个库的表示范围太小了，所以不适用，自己手写吧
def main():
    price_per_pc = 200
    brute_force_speed_per_pc_second = 10 ** 9
    budget = 4 * (10 ** 12)
    total_cipher = 2 ** 128
    amount_mechines = budget / price_per_pc
    time = total_cipher / (amount_mechines * brute_force_speed_per_pc_second)
    format_time(time)


def format_time(time):
    dictionary = {}
    dictionary["time_seconds"] = time
    dictionary["time_minutes"] = dictionary["time_seconds"] / 60
    dictionary["time_hours"] = dictionary["time_minutes"] / 60
    dictionary["time_days"] = dictionary["time_hours"] / 24
    dictionary["time_months"] = dictionary["time_days"] / 30
    dictionary["time_years"] = dictionary["time_months"] / 12
    dictionary["time_billion_years"] = dictionary["time_years"] / (10 ** 9)

    for key, value in dictionary.items():
        print("{0} = {1}".format(key, value))

if __name__ == "__main__":
    main()
```

## 16进制异或问题
```Python
纠结了半天的异或，这是最简单的描述了：
>>> x1 = "e86d2de2"
>>> x2 = "1792d21d"
>>> xor = hex(int(x1, 16) ^ int(x2, 16))

参考：
http://codex.wiki/question/1218903-2917/
http://codex.wiki/question/1165088-1739/


【以下是这道题的code】
__author__ = 'Lin'

List_1 = ["7b50baab 07640c3d", "9d1a4f78 cb28d863", "4af53267 1351e2e1", "e86d2de2 e1387ae9"]
List_2 = ["ac343a22 cea46d60", "75e5e3ea 773ec3e6", "87a40cfa 8dd39154", "1792d21d b645c008"]

# 针对这道题，主要是利用L1 xor L2判断是否全为F，若是，这说明不是secure PRF
def xor(string1, string2):
    return hex(int(string1, 16) ^ int(string2, 16))


def main():
    for i, j in zip(List_1, List_2):
        i = i.split(' ')[0]
        j = j.split(' ')[0]
        if xor(i, j)[2:] == 'f' * len(i):
            print(i, j)


if __name__ == "__main__":
    main()

```

## 也就数一下长度而已
```Python
__author__ = 'Lin'

sentences = [
    'The most direct computation would be for the enemy to try all 2^r possible keys, one by one.',
    'An enciphering-deciphering machine (in general outline) of my invention has been sent to your organization.',
    'To consider the resistance of an enciphering process to being broken we should assume that at same times the enemy knows everything but the key being used and to break it needs only discover the key from this information.',
    'If qualified opinions incline to believe in the exponential conjecture, then I think we cannot afford not to make use of it.'
]


def main():
    for i in range(len(sentences)):
        print("{0}.Sentence = {1}\nLength is {2}\n".format(i + 1, sentences[i], len(sentences[i])))


if __name__ == "__main__":
    main()

```