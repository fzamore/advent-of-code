from common.io import readfile

def isValid(preamble, index, values):
    assert index > preamble - 1, 'bad call to isValid: %d, %d' % (preamble, i)
    s = set()
    for i in range(index - preamble, index):
        s.add(values[i])
    for v in s:
        tv = values[index] - v
        if tv in s:
            return True
    return False

def findAddendsStartingAt(index, values, target):
    i = index
    total = 0
    result = []
    while total < target and i < len(values):
        total += values[i]
        result.append(values[i])
        i += 1
    if total == target:
        return result
    return None

def part1():
    values = []
    for line in readfile('day9.txt'):
        values.append(int(line))

    preamble = 25
    for i in range(preamble, len(values)):
        if not isValid(preamble, i, values):
            print(values[i])
            break

def part2():
    values = []
    for line in readfile('day9.txt'):
        values.append(int(line))

    preamble = 25
    target = None
    for i in range(preamble, len(values)):
        if not isValid(preamble, i, values):
            target = values[i]
            print('target', target)
            break

    for i in range(0, len(values)):
        addends = findAddendsStartingAt(i, values, target)
        if addends != None:
            break

    print('addends', addends)
    print('max/min', max(addends), min(addends))
    print(max(addends) + min(addends))

part2()
