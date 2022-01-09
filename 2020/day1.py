def part2():
    l = []
    with open('day1.txt') as f:
        for line in f.read().splitlines():
            l.append(int(line))

    d = {}
    for i in range(0, len(l)):
        for j in range(i + 1, len(l)):
            v1 = l[i]
            v2 = l[j]
            d[v1 + v2] = (v1, v2)

    for v in l:
        tv = 2020 - v
        if tv in d:
            v1 = v
            v2 = d[tv][0]
            v3 = d[tv][1]
            print(v1, v2, v3, v1 + v2 + v3, v1 * v2 * v3)

def part1():
    with open('day1.txt') as f:
        s = set()
        for line in f.read().splitlines():
            v = int(line)
            tv = 2020 - v
            if tv in s:
                print(v, tv, v * tv)
                return
            s.add(v)

part2()
