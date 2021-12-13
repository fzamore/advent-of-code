from common.sparsegrid import SparseGrid

def foldGrid(grid, fold):
    assert fold[0] == 0 or fold[1] == 0, 'invalid fold: %s' % fold

    d = 0 if fold[1] == 0 else 1
    for coords in grid.getAllCoords():
        if coords[d] > fold[d] and grid.hasValue(coords):
            delta = coords[d] - fold[d]
            newCoord = fold[d] - delta
            if d == 0:
                newCoords = (newCoord, coords[1])
            elif d == 1:
                newCoords = (coords[0], newCoord)
            grid.deleteValue(coords)
            grid.setValue(newCoords, '#')

def part1():
    grid = SparseGrid(2)
    folds = []

    f = open('day13.txt')
    for line in f.readlines():
        line = line[:-1]
        if line == '':
            continue
        elif line[0:4] == 'fold':
            values = line.split(' ')[2].split('=')
            v = int(values[1])
            if values[0] == 'x':
                folds.append((v, 0))
            elif values[0] == 'y':
                folds.append((0, v))
            else:
                print('bad line', line)

        else:
            values = line.split(',')
            assert len(values) == 2, 'bad line %s' % line
            x = int(line.split(',')[0])
            y = int(line.split(',')[1])
            grid.setValue((x, y), '#')
    f.close()

    print(folds)

    foldGrid(grid, folds[0])

    c = 0
    for coords in grid.getAllCoords():
        if grid.hasValue(coords):
            c += 1
    print(c)

def part2():
    grid = SparseGrid(2)
    folds = []

    f = open('day13.txt')
    for line in f.readlines():
        line = line[:-1]
        if line == '':
            continue
        elif line[0:4] == 'fold':
            values = line.split(' ')[2].split('=')
            v = int(values[1])
            if values[0] == 'x':
                folds.append((v, 0))
            elif values[0] == 'y':
                folds.append((0, v))
            else:
                print('bad line', line)

        else:
            values = line.split(',')
            assert len(values) == 2, 'bad line %s' % line
            x = int(line.split(',')[0])
            y = int(line.split(',')[1])
            grid.setValue((x, y), '#')
    f.close()

    print(folds)

    for fold in folds:
        foldGrid(grid, fold)

    grid.print2D(minCoords=[0, 0], maxCoords=[50, 6], default='.')

part2()
