from common.sparsegrid import SparseGrid
from collections import defaultdict

def isValidRegion(r):
    r1 = r[0]
    r2 = r[1]
    return r1[0] <= r2[0] and r1[1] <= r2[1] and r1[2] <= r2[2]

def validateRegion(r):
    assert isValidRegion(r), 'bad region: %s' % str(r)

def countPointsInRegion(r):
    validateRegion(r)
    c1 = r[0]
    c2 = r[1]
    return (c2[0] + 1 - c1[0]) * (c2[1] + 1 - c1[1]) * (c2[2] + 1 - c1[2])

def countPointsInAllRegions(regions):
    return sum([countPointsInRegion(x) for x in regions])

def isOverlappingSegment(a, b):
    assert len(a) == 2 and len(b) == 2, 'isOverlappingSegment takes 1D coords'
    return a[0] <= b[1] and a[1] >= b[0]

def getOverlappingRegion(a, b):
    validateRegion(a)
    validateRegion(b)

    ax1 = a[0][0]
    ay1 = a[0][1]
    az1 = a[0][2]

    ax2 = a[1][0]
    ay2 = a[1][1]
    az2 = a[1][2]

    bx1 = b[0][0]
    by1 = b[0][1]
    bz1 = b[0][2]

    bx2 = b[1][0]
    by2 = b[1][1]
    bz2 = b[1][2]

    if not isOverlappingSegment((ax1, ax2), (bx1, bx2)) or \
       not isOverlappingSegment((ay1, ay2), (by1, by2)) or \
       not isOverlappingSegment((az1, az2), (bz1, bz2)):
        # no overlap
        return None

    return (
        (max(ax1, bx1), max(ay1, by1), max(az1, bz1)),
        (min(ax2, bx2), min(ay2, by2), min(az2, bz2)),
    )

def part1():
    instructions = []
    with open('day22.txt') as f:
        for line in f.read().splitlines():
            values = line.split()
            ranges = values[1].split(',')
            x = ranges[0].split('..')
            y = ranges[1].split('..')
            z = ranges[2].split('..')
            instructions.append((
                1 if values[0] == 'on' else 0,
                ((int(x[0][2:]), int(y[0][2:]), int(z[0][2:])), (int(x[1]), int(y[1]), int(z[1]))),
            ))

    print(instructions)

    grid = SparseGrid(3)
    for (inst, r) in instructions:
        x1 = max(r[0][0], -50)
        x2 = min(r[1][0], 50)
        y1 = max(r[0][1], -50)
        y2 = min(r[1][1], 50)
        z1 = max(r[0][2], -50)
        z2 = min(r[1][2], 50)

        print(x1, x2, y1, y2, z1, z2)

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if inst == 1:
                        grid.setValue((x, y, z), 1)
                    else:
                        grid.deleteValue((x, y, z))

    print(len(grid.getAllCoords()))

def part2():
    instructions = []
    with open('day22.txt') as f:
        for line in f.read().splitlines():
            values = line.split()
            ranges = values[1].split(',')
            x = ranges[0].split('..')
            y = ranges[1].split('..')
            z = ranges[2].split('..')
            instructions.append((
                1 if values[0] == 'on' else 0,
                ((int(x[0][2:]), int(y[0][2:]), int(z[0][2:])), (int(x[1]), int(y[1]), int(z[1]))),
            ))

    print(len(instructions))

    total = 0
    existingRegions = defaultdict(int)
    for instruction, newRegion in instructions:
        validateRegion(newRegion)

        print(instruction, newRegion, countPointsInRegion(newRegion))

        moreRegions = defaultdict(int)
        if instruction == 1:
            # if adding a region, add increment it
            moreRegions[newRegion] += 1

        for existingRegion in existingRegions:
            existingSign = existingRegions[existingRegion]
            overlap = getOverlappingRegion(newRegion, existingRegion)
            if overlap == None:
                # no overlap with existing region; nothing to do
                continue

            assert existingSign <= 1 and existingSign >= -1, 'bad instruction %d' % existingSign

            # cancel out the overlap by flipping its sign
            moreRegions[overlap] += -existingSign

        newRegionTotal = 0
        for region in moreRegions:
            existingRegions[region] += moreRegions[region]
            newRegionTotal += moreRegions[region] * countPointsInRegion(region)
        total += newRegionTotal
        print(newRegionTotal, total)
        print()

    print(total)

part2()
