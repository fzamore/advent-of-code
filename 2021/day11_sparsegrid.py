from common.sparsegrid import SparseGrid

def incrCell(grid, coords):
    v = grid.getValue(coords)
    if v > 9:
        return
    grid.setValue(coords, v + 1)

def resetCell(grid, coords):
    assert grid.getValue(coords) == 10, 'Bad cell value in reset: %d' % grid.getValue(coords)
    grid.setValue(coords, 0)

def flashCell(grid, coords):
    assert grid.getValue(coords) == 10, 'Bad cell value in flash: (%d, %d)' %coords

    if grid.hasMark(coords):
        return 0

    grid.addMark(coords)

    flashes = 1
    for adjCoords in grid.getAdjacentCoordsInGrid(coords):
        v = grid.getValue(adjCoords)
        assert v != None, 'Grid missing value for coords: %s' % str(adjCoords)
        incrCell(grid, adjCoords)
        if v == 9:
            flashes += flashCell(grid, adjCoords)

    return flashes

def step(grid):
    allCoords = list(grid.getAllCoords())
    for coords in allCoords:
        incrCell(grid, coords)

    flashes = 0
    for coords in allCoords:
        if grid.getValue(coords) > 9:
            flashes += flashCell(grid, coords)

    for coords in allCoords:
        if grid.getValue(coords) > 9:
            resetCell(grid, coords)

    grid.clearAllMarks()

    return flashes

def isGridAllZeroes(grid):
    for coords in grid.getAllCoords():
        if grid.getValue(coords) > 0:
            return False
    return True

def part1():
    grid = SparseGrid()
    f = open('day11.txt')
    y = 0
    for line in f.readlines():
        x = 0
        for v in line[:-1]:
            grid.setValue((x, y), int(v))
            x += 1
        y += 1
    f.close()

    grid.print2D()

    flashes = 0
    n = 100
    for i in range(0, n):
        flashes += step(grid)
        print(flashes)
        grid.print2D()

    print(flashes)

def part2():
    grid = SparseGrid()
    f = open('day11.txt')
    y = 0
    for line in f.readlines():
        x = 0
        for v in line[:-1]:
            grid.setValue((x, y), int(v))
            x += 1
        y += 1
    f.close()

    grid.print2D()

    flashes = 0
    n = 3000
    for i in range(0, n):
        flashes += step(grid)
        print(i, flashes)
        grid.print2D()

        if isGridAllZeroes(grid):
            print('all zeroes', i + 1)
            break

part2()
