from common.arraygrid import ArrayGrid

def printGrid(grid):
    grid.print2D({
        1: '>',
        -1: 'v',
        None: '.',
    })

def isCellOccupied(grid, x, y):
    return grid.getValue(x, y) != None

def getNextCell(grid, x, y, v):
    match v:
        case 1:
            nextX = (x + 1) % grid._maxX
            nextY = y
        case -1:
            nextX = x
            nextY = (y + 1) % grid._maxY
        case _:
            assert False, 'bad value passed to getNextCell: %s (%d, %d)' % (v, x, y)

    return (nextX, nextY)

def isNextCellOccupied(grid, x, y, v):
    nextX, nextY = getNextCell(grid, x, y, v)
    return isCellOccupied(grid, nextX, nextY)

def getCellsToMove(grid, value):
    cells = []

    for x in range(0, grid.getMaxX()):
        for y in range(0, grid.getMaxY()):
            v = grid.getValue(x, y)
            if v != value:
                continue
            if not isNextCellOccupied(grid, x, y, v):
                cells.append((x, y))

    return cells

def moveCells(grid, cells, value):
    for x, y in cells:
        nextX, nextY = getNextCell(grid, x, y, value)
        assert grid.getValue(nextX, nextY) == None, \
            'trying to move cell to occupied slot: (%d, %d) => (%d, %d) %s' % \
            (x, y, nextX, nextY, value)
        grid.setValue(nextX, nextY, value)
        grid.setValue(x, y, None)

def stepGrid(grid):
    # east-facing
    eastCellsToMove = getCellsToMove(grid, 1)
    moveCells(grid, eastCellsToMove, 1)

    # south-facing
    southCellsToMove = getCellsToMove(grid, -1)
    moveCells(grid, southCellsToMove, -1)

    return len(eastCellsToMove) + len(southCellsToMove)

def part1():
    with open('day25.txt') as f:
        lines = f.read().splitlines()
    maxX = len(lines[0])
    maxY = len(lines)

    print('grid size', maxX, maxY)

    grid = ArrayGrid(maxX, maxY)
    y = 0
    for line in lines:
        x = 0
        for c in line:
            match c:
                case '>':
                    grid.setValue(x, y, 1)
                case 'v':
                    grid.setValue(x, y, -1)
                case '.':
                    pass
                case _:
                    assert False, 'bad char in line: %s, %s' % (c, line)
            x += 1
        y += 1

    printGrid(grid)

    step = 0
    count = float('inf')
    while count != 0:
        count = stepGrid(grid)
        step += 1

    print(step)

part1()
