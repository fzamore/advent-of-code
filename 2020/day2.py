def part1():
    with open('day2.txt') as f:
        count = 0
        for line in f.read().splitlines():
            v = line.split()
            r1, r2 = v[0].split('-')
            r1 = int(r1)
            r2 = int(r2)
            c = v[1][0]
            p = v[2]

            lc = p.count(c)
            if lc >= r1 and lc <= r2:
                count += 1
                print('valid', line)

        print(count)

def part2():
    with open('day2.txt') as f:
        count = 0
        for line in f.read().splitlines():
            v = line.split()
            p1, p2 = v[0].split('-')
            p1 = int(p1)
            p2 = int(p2)
            c = v[1][0]
            p = v[2]

            c1 = p[p1 - 1] == c
            c2 = p[p2 - 1] == c
            if (c1 and not c2) or (not c1 and c2):
                print('valid', line)
                count += 1

        print(count)

part2()
