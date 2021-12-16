from heapq import heappush, heappop
from collections import defaultdict

def updateTable(table, x, y, path):
    assert path != None, 'updateTable with no path for (%d, %d)' % (x, y)
    table[(x, y)] = path

def getValue(grid, x, y, maxX, maxY):
    assert x >= 0 and x < maxX and y >= 0 and y < maxY, 'Bad coordinate (%d, %d)' % (x, y)
    return grid[y * maxX + x]

# Incorrect algorithm (only considers paths downward and to the right), that
# happens to work for Part 1
def traverse(grid, x, y, maxX, maxY, table):
    if x == maxX - 1 and y == maxY - 1:
        updateTable(table, x, y, [getValue(grid, x, y, maxX, maxY)])
        return

    if (x, y) in table:
        return table[(x, y)]

    if x + 1 < maxX:
        traverse(grid, x + 1, y, maxX, maxY, table)
    if y + 1 < maxY:
        traverse(grid, x, y + 1, maxX, maxY, table)

    pathX = None
    pathY = None
    if x + 1 < maxX:
        pathX = table[(x + 1, y)]
    if y + 1 < maxY:
        pathY = table[(x, y + 1)]

    assert pathX != None or pathY != None, 'Found no best path at (%d, %d)' % (x, y)

    bestPath = None
    if pathX == None:
        bestPath = pathY
    elif pathY == None:
        bestPath = pathX
    else:
        scoreX = sum(pathX)
        scoreY = sum(pathY)
        bestPath = pathX if scoreX < scoreY else pathY

    bestPath = bestPath.copy()
    bestPath.append(getValue(grid, x, y, maxX, maxY))
    updateTable(table, x, y, bestPath)

def printCell5x(grid, x, y, maxX, maxY):
    for i in range(5):
        for j in range(5):
            nx = x + i * maxX
            ny = y + j * maxY
            print(getValue(grid, nx, ny, 5 * maxX, 5 * maxY), end='')
        print()
    print()

def dijkstra(grid, maxX, maxY):
    # min-heap priority queue of points with distance from start as the key
    q = []

    # map from point to distance from start
    d = defaultdict(lambda: float('inf'))

    neighbor_deltas = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    # initialize with the start point
    heappush(q, (0, (0, 0)))
    d[(0, 0)] = 0

    while len(q) > 0:
        p = heappop(q)[1]

        pv = d[p]
        assert d[p] != float('inf'), 'Missing point in dict: %s' % str(p)

        if p[0] == maxX - 1 and p[1] == maxY - 1:
            # done
            return pv

        for (dx, dy) in neighbor_deltas:
            n = (p[0] + dx, p[1] + dy)

            if n[0] < 0 or n[0] >= maxX or n[1] < 0 or n[1] >= maxY:
                continue

            if n in d:
                continue

            nv = getValue(grid, n[0], n[1], maxX, maxY)
            dist = pv + nv
            if dist < d[n]:
                # We've improved the distance to this point. Update the queue
                # and distance map. We don't need to modify its existing entry
                # in the priority queue (if it exists) because the new entry
                # will always be lower, and thus will be popped off the queue
                # before the existing entry.
                d[n] = dist
                heappush(q, (dist, (n)))

    assert False, 'did not find shortest path'

def part1():
    grid = []
    maxX = 0
    maxY = 0
    with open('day15.txt') as f:
        for line in f.read().splitlines():
            maxX = len(line)
            for c in line:
                grid.append(int(c))
            maxY += 1

    print(maxX, maxY)

    table = {}
    startX = 0
    startY = 0
    traverse(grid, startX, startY,  maxX, maxY, table)

    bestPath = table[(startX, startY)]
    bestPath.reverse()
    pathScore = sum(bestPath[1:]) # Don't count the first cell

    print(bestPath)
    print(pathScore)

def part2():
    grid = []
    maxX = 0
    maxY = 0
    with open('day15.txt') as f:
        for line in f.read().splitlines():
            maxX = len(line)
            for c in line:
                grid.append(int(c))
            maxY += 1

    print(maxX, maxY)

    ngrid = [-1] * maxX * maxY * 25
    for x in range(maxX):
        for y in range(maxY):
            value = grid[y * maxX + x]
            for i in range(5):
                for j in range(5):
                    nx = x + i * maxX
                    ny = y + j * maxY

                    nv = value + i + j
                    if nv > 9:
                        nv -= 9
                    assert nv <= 9, 'Bad value in new grid: (%d, %d): %d' %(x, y, value)
                    ngrid[ny * maxX * 5 + nx] = nv

    print(dijkstra(ngrid, maxX * 5, maxY * 5))

part2()
