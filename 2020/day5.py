def partition(seatStr, initialRange, charRange, charMap):
    rMin, rMax = initialRange
    for i in charRange:
        c = seatStr[i]
        r = int((rMax - rMin + 1) / 2)

        assert c in charMap, 'bad char: %s' % c
        if charMap[c] == 1:
            rMin += r
        elif charMap[c] == -1:
            rMax -= r
        else:
            assert False, 'bad charMap: %s' % charMap

    assert rMin == rMax, 'failed to partition: %d, %d' % (rMin, rMax)
    return rMin

def parseSeat(seatStr):
    assert len(seatStr) == 10, 'bad line length: %s' % seatStr

    row = partition(seatStr, (0, 127), range(0, 7), {'B': 1, 'F': -1})
    column = partition(seatStr, (0, 7), range(7, 10), {'R': 1, 'L': -1})
    return row, column

def part1():
    with open('day5.txt') as f:
        maxV = -float('inf')
        for line in f.read().splitlines():
            row, column = parseSeat(line)
            seatV = row * 8 + column
            print(row, column, seatV)
            if seatV > maxV:
                maxV = seatV
        print(maxV)

def part2():
    seatIDs = []
    with open('day5.txt') as f:
        for line in f.read().splitlines():
            row, column = parseSeat(line)
            seatID = row * 8 + column
            print(row, column, seatID)
            seatIDs.append(seatID)

    print('done computing')
    sortedSeatIDs = sorted(seatIDs)
    for i in range(0, len(sortedSeatIDs) - 1):
        if sortedSeatIDs[i] + 1 != sortedSeatIDs[i + 1]:
            print(sortedSeatIDs[i] + 1)

part2()
