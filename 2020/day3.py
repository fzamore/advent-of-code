from common.sparsegrid import SparseGrid

def sled(grid, slope, maxX, maxY):
    print('max', maxX, maxY)

    px, py = 0, 0
    dx, dy = slope

    count = 0
    while py < maxY:
        if grid.hasValue((px, py)):
            count += 1

        px += dx
        py += dy
        if px >= maxX:
            px = px % maxX

    return count

def part1():
    grid = SparseGrid(2)
    with open('day3.txt') as f:
        y = 0
        for line in f.read().splitlines():
            x = 0
            for c in line:
                if c == '#':
                    grid.setValue((x, y), 1)
                x += 1
            y += 1

    #grid.print2D(default='.')
    c = sled(grid, (3, 1), x, y)
    print(c)

def part2():
    grid = SparseGrid(2)
    with open('day3.txt') as f:
        y = 0
        for line in f.read().splitlines():
            x = 0
            for c in line:
                if c == '#':
                    grid.setValue((x, y), 1)
                x += 1
            y += 1

    #grid.print2D(default='.')
    c1 = sled(grid, (1, 1), x, y)
    c2 = sled(grid, (3, 1), x, y)
    c3 = sled(grid, (5, 1), x, y)
    c4 = sled(grid, (7, 1), x, y)
    c5 = sled(grid, (1, 2), x, y)
    print(c1, c2, c3, c4, c5, c1 * c2 * c3 * c4 * c5)

part2()
