from common.sparsegrid import SparseGrid

# tick in n dimensions
def tickND(grid, dim):
    newgrid = SparseGrid(dim)

    # Add 1 value in each direction (inclusive) for each dimension
    minCoords = [x - 1 for x in grid.getMinCoords()]
    maxCoords = [x + 2 for x in grid.getMaxCoords()]

    for coords in grid.getAllCoordsInOrder(minCoords, maxCoords):
        neighbors = 0
        for adjCoords in grid.getAdjacentCoords(coords):
            if grid.hasValue(adjCoords):
                neighbors += 1
        if neighbors in [2, 3] and grid.hasValue(coords):
            newgrid.setValue(coords, 1)
        elif neighbors == 3 and not grid.hasValue(coords):
            newgrid.setValue(coords, 1)

    return newgrid

def tick3D(grid):
    newgrid = SparseGrid(3)

    minCoords = grid.getMinCoords()
    maxCoords = grid.getMaxCoords()

    for x in range(minCoords[0] - 1, maxCoords[0] + 2):
        for y in range(minCoords[1] - 1, maxCoords[1] + 2):
            for z in range(minCoords[2] - 1, maxCoords[2] + 2):
                neighbors = 0
                for adjCoords in grid.getAdjacentCoords((x, y, z)):
                    if grid.hasValue(adjCoords):
                        neighbors += 1
                if neighbors in [2, 3] and grid.hasValue((x, y, z)):
                    newgrid.setValue((x, y, z), 1)
                elif neighbors == 3 and not grid.hasValue((x, y, z)):
                    newgrid.setValue((x, y, z), 1)

    return newgrid

def part1():
    f = open('day17.txt')
    grid = SparseGrid(3)
    y = 0
    for line in f.readlines():
        x = 0
        for v in line[:-1]:
            if v == '#':
                grid.setValue((x, y, 0), 1)
            x += 1
        y += 1
    f.close()

    grid.print2DSlices(default=0)

    n = 6
    for i in range(0, n):
        grid = tick3D(grid)

    grid.print2DSlices(default=0)

    count = 0
    for coords in grid.getAllCoords():
        if grid.hasValue(coords):
            count += 1
    print(count)

def part2():
    f = open('day17.txt')
    grid = SparseGrid(4)
    y = 0
    for line in f.readlines():
        x = 0
        for v in line[:-1]:
            if v == '#':
                grid.setValue((x, y, 0, 0), 1)
            x += 1
        y += 1
    f.close()

    n = 6
    for i in range(0, n):
        grid = tickND(grid, 4)
        print('done', i)

    count = 0
    for coords in grid.getAllCoords():
        if grid.hasValue(coords):
            count += 1
    print(count)

part2()
