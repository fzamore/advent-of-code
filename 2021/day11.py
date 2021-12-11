def getGridIndex(grid, x, y):
    if x < 0 or y < 0 or x >= grid['MAXx'] or y >= grid['MAXy']:
        return -1
    return y * grid['MAXx'] + x

def getCellValue(grid, x, y):
    i = getGridIndex(grid, x, y)
    if i < 0:
        return -1
    return grid['data'][i]

def incrCell(grid, x, y):
    i = getGridIndex(grid, x, y)
    if i < 0:
        return
    if getCellValue(grid, x, y) > 9:
        return
    grid['data'][i] += 1

def resetCell(grid, x, y):
    assert getCellValue(grid, x, y) == 10, 'Bad cell value in reset: %d' % getCellValue(grid, x, y)
    i = getGridIndex(grid, x, y)
    assert i >= 0 and i < len(grid['data']), 'Bad grid index in reset: %d (%d, %d)' %(i, x, y)
    grid['data'][getGridIndex(grid, x, y)] = 0

def flashCell(grid, x, y):
    assert getCellValue(grid, x, y) == 10, 'Bad cell value in flash: (%d, %d)' %(x, y)
    if '%d,%d' % (x, y) in grid['flashes']:
        return 0

    grid['flashes']['%d,%d' %(x, y)] = 1

    flashes = 1
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx = x + dx
            ny = y + dy
            v = getCellValue(grid, nx, ny)
            incrCell(grid, nx, ny)
            if v == 9:
                flashes += flashCell(grid, nx, ny)

    return flashes

def printGrid(grid):
    for y in range(0, grid['MAXy']):
        for x in range(0, grid['MAXx']):
            print(getCellValue(grid, x, y), end='')
        print()
    print()

def step(grid):
    for x in range(0, grid['MAXx']):
        for y in range(0, grid['MAXy']):
            incrCell(grid, x, y)

    flashes = 0
    for x in range(0, grid['MAXx']):
        for y in range(0, grid['MAXy']):
            if getCellValue(grid, x, y) > 9:
                flashes += flashCell(grid, x, y)

    for x in range(0, grid['MAXx']):
        for y in range(0, grid['MAXy']):
            if getCellValue(grid, x, y) > 9:
                resetCell(grid, x, y)
    grid['flashes'] = {}

    return flashes

def isGridAllZeroes(grid):
    for x in range(0, grid['MAXx']):
        for y in range(0, grid['MAXy']):
            if getCellValue(grid, x, y) > 0:
                return False
    return True

def part1():
    grid = {
        'MAXx': 10,
        'MAXy': 10,
        'data': [],
        'flashed': {},
    }
    f = open('day11.txt')
    for line in f.readlines():
        for v in line[:-1]:
            grid['data'].append(int(v))
    f.close()

    printGrid(grid)

    flashes = 0
    n = 100
    for i in range(0, n):
        flashes += step(grid)
        print(flashes)
        printGrid(grid)

    print(flashes)

def part2():
    grid = {
        'MAXx': 10,
        'MAXy': 10,
        'data': [],
        'flashed': {},
    }
    f = open('day11.txt')
    for line in f.readlines():
        for v in line[:-1]:
            grid['data'].append(int(v))
    f.close()

    printGrid(grid)

    flashes = 0
    n = 3000
    for i in range(0, n):
        flashes += step(grid)
        print(i, flashes)
        printGrid(grid)

        if isGridAllZeroes(grid):
            print('all zeroes', i + 1)
            break

    print(flashes)

part2()
