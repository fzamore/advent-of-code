from collections import defaultdict

def step(word, pairs):
    result = [word[0]]
    i = 0
    for i in range(len(word) - 1):
        key = '%s%s' % (word[i], word[i + 1])
        if key in pairs:
            result.append(pairs[key])
        result.append(word[i + 1])

    return result

def step2(paircounts, pairs):
    result = defaultdict(int)
    for key in paircounts:
        if key in pairs:
            result['%s%s' % (key[0], pairs[key])] += paircounts[key]
            result['%s%s' % (pairs[key], key[1])] += paircounts[key]
    return result

def part1():
    word = []
    pairs = {}
    f = open('day14.txt')
    for line in f.readlines():
        line = line.strip()
        if len(line) == 0:
            continue

        if len(word) == 0:
            for c in line:
                word.append(c)
        else:
            values = line.split(' -> ')
            pairs[values[0]] = values[1]

    f.close()

    print(word)
    print(pairs)

    for i in range(10):
        word = step(word, pairs)

    #print(''.join(word))
    print(len(word))
    d = defaultdict(int)
    for c in word:
        d[c] += 1

    mc = 0
    lc = 10000000000
    mchar = ''
    lchar = ''
    for c in d:
        if d[c] > mc:
            mc = d[c]
            mchar = c
        if d[c] < lc:
            lc = d[c]
            lchar = c

    print(d)
    print(mchar, lchar,  mc - lc)

def part2():
    paircounts = defaultdict(int)
    pairs = {}
    lastchar = ''
    with open('day14.txt') as f:
        word = f.readline().strip()
        for i in range(len(word) - 1):
            key = '%s%s' % (word[i], word[i + 1])
            paircounts[key] += 1
        lastchar = word[-1]

        f.readline() # skip blank line

        for line in f.read().splitlines():
            values = line.split(' -> ')
            pairs[values[0]] = values[1]

    print(paircounts)
    for i in range(40):
        paircounts = step2(paircounts, pairs)
        d = defaultdict(int)

    d = defaultdict(int)
    for pair in paircounts:
        # count the first character in each pair
        d[pair[0]] += paircounts[pair]

    # special-case the last char of the entire string
    print('lastchar:', lastchar)
    d[lastchar] += 1

    mchar = max(d, key=d.get)
    lchar = min(d, key=d.get)

    print(d)
    print('most:', mchar, d[mchar])
    print('least:', lchar, d[lchar])
    print(d[mchar] - d[lchar])

part2()
