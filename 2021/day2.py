def part1():
    hpos = 0
    vpos = 0
    f = open('day2.txt')
    for line in f.readlines():
        tokens = line.split()
        if len(tokens) != 2:
            print('Invalid line: %s' % line)
            continue
        if tokens[0] == 'forward':
            hpos += int(tokens[1])
        elif tokens[0] == 'down':
            vpos += int(tokens[1])
        elif tokens[0] == 'up':
            vpos -= int(tokens[1])

    print(hpos, vpos, hpos * vpos)
    f.close()

def part2():
    hpos = 0
    vpos = 0
    aim = 0
    f = open('day2.txt')
    for line in f.readlines():
        tokens = line.split()
        if len(tokens) != 2:
            print('Invalid line: %s' % line)
            continue
        v = int(tokens[1])
        if tokens[0] == 'forward':
            hpos += v
            vpos += aim * v
        elif tokens[0] == 'down':
            aim += v
        elif tokens[0] == 'up':
            aim -= v

    print(hpos, vpos, aim, hpos * vpos)
    f.close()


part2()
