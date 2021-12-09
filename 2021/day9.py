def getGridValue(grid, x, y):
    if x < 0 or y < 0 or x >= grid['MAXx'] or y >= grid['MAXy']:
        return 10

    return grid['data'][y * grid['MAXx'] + x]

def isLowestPoint(grid, x, y):
    v = getGridValue(grid, x, y)
    if v >= getGridValue(grid, x + 1, y):
        return False
    if v >= getGridValue(grid, x - 1, y):
        return False
    if v >= getGridValue(grid, x, y + 1):
        return False
    if v >= getGridValue(grid, x, y - 1):
        return False

    return True

def printGrid(grid):
    print(grid['MAXx'], grid['MAXy'])
    for y in range(0, grid['MAXy']):
        for x in range(0, grid['MAXx']):
            print('%s' % getGridValue(grid, x, y), end='')
        print()
    print()

def markGridCell(grid, x, y):
    grid['marked']['%s,%s' %(x, y)] = 1

def isGridCellMarked(grid, x, y):
    return '%s,%s' % (x, y) in grid['marked']

def getBasinSize(grid, x, y):
    if isGridCellMarked(grid, x, y):
        return 0

    markGridCell(grid, x, y)
    if getGridValue(grid, x, y) > 8:
        return 0

    size = 1

    for di in range(-1, 2):
        for dj in range(-1, 2):
            if di == 0 and dj == 0:
                continue

            if di == 0 or dj == 0:
                # horizontal / vertical
                size += getBasinSize(grid, x + di, y + dj)
            elif getGridValue(grid, x + di, y) < 9 or getGridValue(grid, x, y + dj) < 9:
                # diagonal
                size += getBasinSize(grid, x + di, y + dj)
                pass

    return size

def part1():
    f = open('day9.txt')
    lines = f.readlines()
    f.close()

    grid = {
        'data': [],
        'MAXy': len(lines),
    }

    for line in lines:
        line = line[:-1]
        m = len(line)
        if 'MAXx' in grid and grid['MAXx'] != m:
            print('Bad line: %s, %d, %d' % (line, m, grid['MAXx']))
            break
        grid['MAXx'] = m
        for v in line:
            grid['data'].append(int(v))

    risklevelsum = 0
    for x in range(0, grid['MAXx']):
        for y in range(0, grid['MAXy']):
            if isLowestPoint(grid, x, y):
                v = getGridValue(grid, x, y)
                assert v != 10
                risklevelsum += v + 1

    print(risklevelsum)

def part2():
    f = open('day9.txt')
    lines = f.readlines()
    f.close()

    grid = {
        'data': [],
        'MAXy': len(lines),
        'marked': {},
    }

    for line in lines:
        line = line[:-1]
        m = len(line)
        if 'MAXx' in grid and grid['MAXx'] != m:
            print('Bad line: %s, %d, %d' % (line, m, grid['MAXx']))
            break
        grid['MAXx'] = m
        for v in line:
            grid['data'].append(int(v))

    basins = []
    for x in range(0, grid['MAXx']):
        for y in range(0, grid['MAXy']):
            basinSize = getBasinSize(grid, x, y)
            if basinSize > 0:
                print('BasinSize:', x, y, basinSize)
                basins.append(basinSize)

    sortedBasins = sorted(basins)
    sortedBasins.reverse()
    print(sortedBasins[0] * sortedBasins[1] * sortedBasins[2])

part2()
