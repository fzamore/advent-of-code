def part1():
    f = open('day3.txt')
    vals = [0,0,0,0,0,0,0,0,0,0,0,0]
    for line in f.readlines():
        line = line[:-1]
        if len(line) != 12:
            print('bad line: %s' % line)
        for i in range(0, len(line)):
            bit = line[i]
            if bit == '0':
                vals[i] -= 1
            elif bit == '1':
                vals[i] += 1
            else:
                print('bad line: %s' % line)
                continue

    f.close()

    gamma = ''
    epsilon = ''
    for v in vals:
        if v < 0:
            gamma += '0'
            epsilon += '1'
        elif v > 0:
            gamma += '1'
            epsilon += '0'
        else:
            print('Even parity: %s' % vals)

    gv = int(gamma, 2)
    ev = int(epsilon, 2)
    print(gamma, epsilon, gv, ev, gv * ev)

def part2_helper(data, k, tie):
    if len(data) == 1:
        return data[0]

    total = 0
    for v in data:
        if v[k] == '0':
            total -= 1
        elif v[k] == '1':
            total += 1
        else:
            print('bad datum: %s' %v)

    if total < 0:
        w = '0' if tie == '1' else '1'
    elif total > 0:
        w = '1' if tie == '1' else '0'
    else:
        w = tie

    result = []
    for v in data:
        if v[k] == w:
            result.append(v)
    return part2_helper(result, k + 1, tie)

def part2():
    f = open('day3.txt')
    data = []
    for line in f.readlines():
        data.append(line[:-1])
    f.close()

    o2 = part2_helper(data, 0, '1')
    co2 = part2_helper(data, 0, '0')

    o2v = int(o2, 2)
    co2v = int(co2, 2)
    print(o2, co2, o2v, co2v, o2v * co2v)

part2()
