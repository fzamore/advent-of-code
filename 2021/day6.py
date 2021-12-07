def part1():
    f = open('day6.txt')
    data = list(map(int, f.readlines()[0].split(',')))
    f.close()

    n = 80
    for i in range(0, n):
        newdata = []
        newfish = 0
        for oldv in data:
            if oldv == 0:
                newv = 6
                newfish += 1
            else:
                newv = oldv - 1
            newdata.append(newv)
        newdata.extend([8 for x in range(0, newfish)])

        data = newdata

    print(len(data))

def initmap():
    m = {}
    for i in range(0, 7):
        m[i] = 0
    return m

def part2():
    f = open('day6.txt')
    data = list(map(int, f.readlines()[0].split(',')))
    f.close()

    m = initmap()
    for v in data:
        m[v] += 1

    n = 256
    for i in range(0, n):
        newm = initmap()
        newm[7] = 0
        newm[8] = 0
        for k in m:
            if k != 0:
                newm[k - 1] += m[k]
            else:
                newm[8] += m[k]
                newm[6] += m[k]

        m = newm

    print(sum(m.values()))

part2()
