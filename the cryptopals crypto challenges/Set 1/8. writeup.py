from collections import Counter


# writeUp这里有点问题，如果 blocksize = 16 的话就不适用AES了，AES是16字节而不是8字节（16的话是16个十六进制数）

def main():
    blocksize = 16

    # 参数'rU'，可以避免unix和windowx下换行符表示不同的问题(\r\n, \n)
    with open('challenge8.txt', 'rU') as f:
        # Read all lines available on the input stream and return them as a list of lines
        lines = f.readlines()

    # 这种分组方式可以学习一下
    for line in (l.strip() for l in lines):
        # list(range(0, 16 * 5, 16)) = [0, 16, 32, 48 ...], end够范围才有索引test(0, 16 * 5 + 1)
        indexes = range(0, len(line), blocksize)

        d = []
        for (start, end) in zip(indexes, indexes[1:]):
            d.append(line[start:end])

        # Counter('abcdeabcdabcaba').most_common(3)
        # 3表示，列举出3个出现次数最多的元素。
        cn = Counter(d)
        for each in cn.most_common():
            if each[1] > 1:
                print(each)
            else:
                break
        """
        这里得改进一下，这里判断条件只判断的最大值＞1的那一行，然后就把一整行的结果输出出来了
        if cn.most_common()[0][1] > 1:
            print(cn)
        """


if __name__ == "__main__":
    main()
