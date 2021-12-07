
def part1():
    f = open('day1.txt')
    prev = 100000000
    total = 0
    for line in f.readlines():
        cur = int(line)
        if cur > prev:
            total += 1
        prev = cur

    print(total)
    f.close()

def part2():
    f = open('day1.txt')
    prev = 10000000
    total = 0
    lines = f.readlines()
    for i in range(0, len(lines) - 2):
        cur = int(lines[i]) + int(lines[i+1]) + int(lines[i+2])
        if cur > prev:
            total += 1
        prev = cur

    print(total)
    f.close()

part2()
