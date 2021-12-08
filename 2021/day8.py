def part1():
    f = open('day8.txt')
    data = f.readlines()
    f.close()

    c = 0
    for line in data:
        v1 = line.split(' | ')
        output = v1[1].split()
        for v in output:
            if len(v) == 2 or len(v) == 3 or len(v) == 4 or len(v) == 7:
                c += 1

    print(c)

def storeDigit(wordValues, digitValues, word, digit):
    if digit in digitValues and digitValues[digit] != word:
        print()
        print('*******BAD DIGIT: %d, %s, %s, %d' % (digit, word, digitValues[digit], wordValues[digitValues[digit]]))
        print(digitValues)
        print(wordValues)
        print()
        assert False
    digitValues[digit] = word
    wordValues[word] = digit

def decode(data, output):
    # Canonicalize by sorting.
    data = list(map(lambda x: ''.join(sorted(x)), data))
    output = list(map(lambda x: ''.join(sorted(x)), output))

    wordValues = {}
    for word in data:
        l = len(word)
        if l == 2:
            wordValues[word] = 1
        elif l == 3:
            wordValues[word] = 7
        elif l == 4:
            wordValues[word] = 4
        elif l == 7:
            wordValues[word] = 8

    digitValues = dict((v,k) for k,v in wordValues.items())

    for word in data:
        l = len(word)
        if l == 5:
            # 2, 3, 5
            if len(set(digitValues[1]).intersection(word)) == 2:
                storeDigit(wordValues, digitValues, word, 3)
            elif len(set(digitValues[4]).intersection(word)) == 3:
                storeDigit(wordValues, digitValues, word, 5)
            elif len(set(digitValues[4]).intersection(word)) == 2:
                storeDigit(wordValues, digitValues, word, 2)
            else:
                assert False
        elif l == 6:
            # 0, 6, 9. Ordering is important: 6 must come first.
            if len(set(digitValues[7]).intersection(word)) == 2:
                storeDigit(wordValues, digitValues, word, 6)
            elif len(set(digitValues[4]).intersection(word)) == 4:
                storeDigit(wordValues, digitValues, word, 9)
            elif len(set(digitValues[4]).intersection(word)) == 3:
                storeDigit(wordValues, digitValues, word, 0)
            else:
                assert False

    result = 0
    exp = 0
    output.reverse()
    for word in output:
        result += wordValues[word] * pow(10, exp)
        exp += 1

    print(wordValues)
    print(digitValues)
    print(output)
    print(result)
    print()

    return result

def part2():
    f = open('day8.txt')
    lines = f.readlines()
    f.close()

    result = 0
    for line in lines:
        line = line[:-1]
        v1 = line.split(' | ')
        result += decode(v1[0].split() + v1[1].split(), v1[1].split())

    print(result)

part2()
