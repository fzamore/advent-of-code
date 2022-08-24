from common.readfile import readfile
from common.sparsegrid import SparseGrid

def countAllOccupiedSeats(grid):
    return len([x for x in grid.getAllCoords() if grid.getValue(x) == 1])

def countAdjacentOccupiedSeats(grid, x, y):
    count = 0
    for coords in grid.getAdjacentCoordsInGrid((x, y)):
        if grid.getValue(coords) == 1:
            count += 1
    return count

def countLineOfSightOccupiedSeats(grid, x, y):
    minCoords = grid.getMinCoords()
    maxCoords = grid.getMaxCoords()

    deltas = [-1, 0, 1]
    count = 0
    for dx in deltas:
        for dy in deltas:
            if dx == 0 and dy == 0:
                continue
            i = 1
            while True:
                nx = dx * i + x
                ny = dy * i + y
                if nx < minCoords[0] or nx > maxCoords[0] or ny < minCoords[1] or ny > maxCoords[1]:
                    break
                value = grid.getValue((nx, ny))
                if value == None:
                    i += 1
                    continue
                if value == 1:
                    count += 1
                break
    return count

def iterate(grid, threshold, countOccupiedSeats):
    newgrid = SparseGrid(2)
    changed = 0
    for x, y in grid.getAllCoords():
        value = grid.getValue((x, y))
        assert value in [0, 1], 'bad grid value: (%d, %d), %s' % (x, y, value)
        occupied = countOccupiedSeats(grid, x, y)
        if value == 0 and occupied == 0:
            value = 1
            changed += 1
        elif value == 1 and occupied >= threshold:
            value = 0
            changed += 1
        newgrid.setValue((x, y), value)
    return newgrid, changed

def part1():
    grid = SparseGrid(2)
    y = 0
    for line in readfile('day11.txt'):
        x = 0
        for c in line:
            if c == 'L':
                grid.setValue((x, y), 0)
            x += 1
        y += 1

    grid.print2D(default='.')

    grid, changed = iterate(grid, 4, countAdjacentOccupiedSeats)
    steps = 1
    print(steps, changed)

    while changed > 0:
        grid, changed = iterate(grid, 4, countAdjacentOccupiedSeats)
        steps += 1
        print(steps, changed)

    print()
    grid.print2D(default='.')
    print(changed)
    print(steps)
    print(countAllOccupiedSeats(grid))

def part2():
    grid = SparseGrid(2)
    y = 0
    for line in readfile('day11.txt'):
        x = 0
        for c in line:
            if c == 'L':
                grid.setValue((x, y), 0)
            x += 1
        y += 1

    grid.print2D(default='.')

    grid, changed = iterate(grid, 5, countLineOfSightOccupiedSeats)
    steps = 1
    print(steps, changed)

    while changed > 0:
        grid, changed = iterate(grid, 5, countLineOfSightOccupiedSeats)
        steps += 1
        print(steps, changed)

    print()
    grid.print2D(default='.')
    print(changed)
    print(steps)
    print(countAllOccupiedSeats(grid))

part2()
