from common.readfile import readfile

def countSequences(values, i, table):
    l = len(values)
    if i == l - 1:
        return 1

    # memoize
    if i in table:
        return table[i]

    result = 0
    v = values[i]
    if i < l - 1 and values[i + 1] - v in [1, 2, 3]:
        r = countSequences(values, i + 1, table)
        table[i + 1] = r
        result += r
    if i < l - 2 and values[i + 2] - v in [1, 2]:
        r = countSequences(values, i + 2, table)
        table[i + 2] = r
        result += r
    if i < l - 3 and values[i + 3] - v in [3]:
        r = countSequences(values, i + 3, table)
        table[i + 3] = r
        result += r

    return result

def part1():
    values = sorted([int(x) for x in readfile('day10.txt')])
    values = [0] + values + [values[-1] + 3]
    print(values)

    ones = 0
    threes = 0
    for i in range(0, len(values) - 1):
        diff = values[i + 1] - values[i]
        if diff == 1:
            ones += 1
        elif diff == 3:
            threes += 1
        else:
            assert False, 'bad input: %d, %d, %d' %(i, values[i], values[i + 1])

    print(ones, threes, ones * threes)

def part2():
    values = sorted([int(x) for x in readfile('day10.txt')])
    values = [0] + values + [values[-1] + 3]
    print(len(values))

    ans = countSequences(values, 0, {})
    print(ans)

part2()
