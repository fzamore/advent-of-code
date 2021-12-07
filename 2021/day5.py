def incr(grid, x, y):
    key = '%s,%s' % (x, y)
    if key not in grid:
        grid[key] = 0
    grid[key] += 1

def part1():
    grid = {}
    f = open('day5.txt')
    for line in f.readlines():
        coords = line.split(' -> ')
        x1 = int(coords[0].split(',')[0])
        y1 = int(coords[0].split(',')[1])
        x2 = int(coords[1].split(',')[0])
        y2 = int(coords[1].split(',')[1])
        if x1 != x2 and y1 != y2:
            continue

        if x1 == x2:
            start = min(y1, y2)
            end = max(y1, y2)
            for i in range(start, end + 1):
                incr(grid, x1, i)
        elif y1 == y2:
            start = min(x1, x2)
            end = max(x1, x2)
            for i in range(start, end + 1):
                incr(grid, i, y1)

    f.close()

    print(len([x for x in list(grid.values()) if x > 1]))

def part2():
    grid = {}
    f = open('day5.txt')
    for line in f.readlines():
        coords = line.split(' -> ')
        x1 = int(coords[0].split(',')[0])
        y1 = int(coords[0].split(',')[1])
        x2 = int(coords[1].split(',')[0])
        y2 = int(coords[1].split(',')[1])
        c = max(x1, x2) - min(x1, x2)

        if x1 == x2:
            dx = 0
            c = max(y1, y2) - min(y1, y2)
        elif x1 < x2:
            dx = 1
        else:
            dx = -1

        if y1 == y2:
            dy = 0
        elif y1 < y2:
            dy = 1
        else:
            dy = -1

        i = x1
        j = y1
        for n in range(0, c + 1):
            incr(grid, i, j)
            i += dx
            j += dy

    f.close()

    print(len([x for x in list(grid.values()) if x > 1]))

part2()
