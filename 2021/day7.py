from collections import defaultdict

def part1():
    f = open('day7.txt')
    data = list(map(int, f.readlines()[0].split(',')))
    f.close()

    m = defaultdict(int)
    for i in range(0, max(data)):
        for d in data:
            m[i] += abs(d - i)

    minv = 100000000
    mink = -1
    for k in m:
        if m[k] < minv:
            mink = k
            minv = m[k]

    print(max(data), len(data), end=' ')
    print(mink, minv)

def sum1toN(n):
    return int((n + 1) * n / 2)

def part2():
    f = open('day7.txt')
    data = list(map(int, f.readlines()[0].split(',')))
    f.close()

    m = defaultdict(int)
    for i in range(0, max(data)):
        for d in data:
            m[i] += sum1toN(abs(d - i))

    minv = 100000000
    mink = -1
    for k in m:
        if m[k] < minv:
            mink = k
            minv = m[k]

    print(max(data), len(data))
    print(mink, minv)

part2()
