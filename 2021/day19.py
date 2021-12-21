from collections import defaultdict

def multiplyTuple(t1, t2):
    return tuple(e1 * e2 for e1, e2 in zip(t1, t2))

def subtractTuple(t1, t2):
    return tuple(e1 - e2 for e1, e2 in zip(t1, t2))

def addTuple(t1, t2):
    return tuple(e1 + e2 for e1, e2 in zip(t1, t2))

def getCoordTransforms():
    return [
        lambda c: (c[0], c[1], c[2]), # (x, y, z)
        lambda c: (c[0], c[2], -c[1]), # (x, z, -y),
        lambda c: (c[0], -c[1], -c[2]), # (x, -y, -z),
        lambda c: (c[0], -c[2], c[1]), # (x, -z, y),

        lambda c: (-c[0], c[1], -c[2]), # (-x, y, -z),
        lambda c: (-c[0], -c[2], -c[1]), # (-x, -z, -y),
        lambda c: (-c[0], -c[1], c[2]), # (-x, -y, z),
        lambda c: (-c[0], c[2], c[1]), # (-x, z, y),

        lambda c: (c[1], c[2], c[0]), # (y, z, x),
        lambda c: (c[1], c[0], -c[2]), # (y, x, -z),
        lambda c: (c[1], -c[2], -c[0]), # (y, -z, -x),
        lambda c: (c[1], -c[0], c[2]), # (y, -x, z),

        lambda c: (-c[1], c[0], c[2]), # (-y, x, z),
        lambda c: (-c[1], c[2], -c[0]), # (-y, z, -x),
        lambda c: (-c[1], -c[0], -c[2]), # (-y, -x, -z),
        lambda c: (-c[1], -c[2], c[0]), # (-y, -z, x),

        lambda c: (c[2], c[0], c[1]), # (z, x, y),
        lambda c: (c[2], c[1], -c[0]), # (z, y, -x),
        lambda c: (c[2], -c[0], -c[1]), # (z, -x, -y),
        lambda c: (c[2], -c[1], c[0]), # (z, -y, x),

        lambda c: (-c[2], c[1], c[0]), # (-z, y, x),
        lambda c: (-c[2], c[0], -c[1]), # (-z, x, -y),
        lambda c: (-c[2], -c[1], -c[0]), # (-z, -y, -x),
        lambda c: (-c[2], -c[0], c[1]), # (-z, -x, y),
    ]

def getCoordVariants(coords):
    x = coords[0]
    y = coords[1]
    z = coords[2]
    return [
        (x, y, z),
        (x, z, -y),
        (x, -y, -z),
        (x, -z, y),

        (-x, y, -z),
        (-x, -z, -y),
        (-x, -y, z),
        (-x, z, y),

        (y, z, x),
        (y, x, -z),
        (y, -z, -x),
        (y, -x, z),

        (-y, x, z),
        (-y, z, -x),
        (-y, -x, -z),
        (-y, -z, x),

        (z, x, y),
        (z, y, -x),
        (z, -x, -y),
        (z, -y, x),

        (-z, y, x),
        (-z, x, -y),
        (-z, -y, -x),
        (-z, -x, y),
    ]

def transformCoordinates(coordList, transform):
    return [transform(x) for x in coordList]

def computePairwiseDeltas(beacons):
    d = {}
    for i in range(len(beacons)):
        for j in range(i + 1, len(beacons)):
            d[(i, j)] = subtractTuple(beacons[j], beacons[i])
            d[(j, i)] = subtractTuple(beacons[i], beacons[j])

    #result = defaultdict(list)
    result = {}
    for pair in d:
        #for delta in d[pair]:
        #result[delta].append((beacons[pair[1]], beacons[pair[0]]))
        delta = d[pair]
        if delta in result:
            print('WARNING, delta already in result', delta, result[delta])
        #result[delta] = beacons[pair[0]]
        # store the beacon index that's responsible for this delta
        result[delta] = pair[0]

    return result

def getScannerPosition(scanners, i1, i2):
    beacons1 = scanners[i1]
    beacons2 = scanners[i2]
    d1 = computePairwiseDeltas(beacons1)
    for transform in getCoordTransforms():
        d2 = computePairwiseDeltas(transformCoordinates(beacons2, transform))

        # change to defaultdict(set)?
        possibleMatches = defaultdict(lambda: defaultdict(int))

        for index in d1:
            if index in d2:
                beacon1 = beacons1[d1[index]]
                beacon2 = beacons2[d2[index]]
                possibleMatches[beacon1][beacon2] += 1

        if len(possibleMatches) == 12:
            # We found 12 overlapping beacons
            scannerPosition = None
            scannerTransform = None

            for beacon1 in possibleMatches:
                assert len(possibleMatches[beacon1]) > 0, 'no matches for beacon: %s' % beacon1
                if len(possibleMatches[beacon1]) > 1:
                    print('WARNING, multiple matches found for beacon:', beacon1)

                beacon2 = list(possibleMatches[beacon1].keys())[0]

                transformed = transform(beacon2)
                if scannerPosition == None:
                    scannerPosition = subtractTuple(beacon1, transformed)
                    scannerTransform = transform

                assert scannerPosition == subtractTuple(beacon1, transformed), \
                    'Multiple scanner positions found: %s, %s' % (
                        scannerPosition,
                        subtractTuple(beacon1, transformed),
                    )

            return scannerPosition, scannerTransform

    return None, None

def transformBeacons(beacons, position, transform):
    for i in range(0, len(beacons)):
        beacons[i] = addTuple(transform(beacons[i]), position)

def computeManhattanDistance(c1,  c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])

def part1():
    scanners = defaultdict(list)
    scanner = -1
    with open('day19.txt') as f:
        for line in f.read().splitlines():
            if line == '':
                continue
            coords = line.split(',')
            if len(coords) == 3:
                assert scanner != -1, 'did not find scanner for coords: %s' % line
                scanners[scanner].append((int(coords[0]), int(coords[1]), int(coords[2])))
            else:
                parts = line.split()
                assert len(parts) == 4, 'bad line: %s' % line
                scanner = int(parts[2])

    print('beacons per scanner:', len(scanners[0]))
    print()

    allBeacons = set(scanners[0])
    scannerPositions = {0: (0, 0, 0)}
    while len(scannerPositions) < len(scanners):
        for i in range(0, len(scanners)):
            if i not in scannerPositions:
                continue
            for j in range(0, len(scanners)):
                if j in scannerPositions:
                    continue
                scannerPosition, scannerTransform = getScannerPosition(scanners, i, j)
                if scannerPosition == None:
                    continue

                print('Scanner position', j, scannerPosition)
                scannerPositions[j] = scannerPosition

                # transform all beacons for the found scanner
                transformBeacons(scanners[j], scannerPosition, scannerTransform)
                for beacon in scanners[j]:
                    allBeacons.add(beacon)

                assert (len(set(scanners[i]).intersection(set(scanners[j])))) == 12, \
                    'did not find overlap in %d, %d' %(i, j)

    print('total beacons', len(allBeacons))

def part2():
    scanners = defaultdict(list)
    scanner = -1
    with open('day19.txt') as f:
        for line in f.read().splitlines():
            if line == '':
                continue
            coords = line.split(',')
            if len(coords) == 3:
                assert scanner != -1, 'did not find scanner for coords: %s' % line
                scanners[scanner].append((int(coords[0]), int(coords[1]), int(coords[2])))
            else:
                parts = line.split()
                assert len(parts) == 4, 'bad line: %s' % line
                scanner = int(parts[2])

    print('beacons per scanner:', len(scanners[0]))
    print()

    allBeacons = set(scanners[0])
    scannerPositions = {0: (0, 0, 0)}
    while len(scannerPositions) < len(scanners):
        for i in range(0, len(scanners)):
            if i not in scannerPositions:
                continue
            for j in range(0, len(scanners)):
                if j in scannerPositions:
                    continue
                scannerPosition, scannerTransform = getScannerPosition(scanners, i, j)
                if scannerPosition == None:
                    continue

                print('Scanner position', j, scannerPosition)
                scannerPositions[j] = scannerPosition

                # transform all beacons for the found scanner
                transformBeacons(scanners[j], scannerPosition, scannerTransform)
                for beacon in scanners[j]:
                    allBeacons.add(beacon)

                assert (len(set(scanners[i]).intersection(set(scanners[j])))) == 12, \
                    'did not find overlap in %d, %d' %(i, j)

    print('total beacons', len(allBeacons))

    maxM = -float('inf')
    for i in range(len(scanners)):
        for j in range(i + 1, len(scanners)):
            m = computeManhattanDistance(scannerPositions[i], scannerPositions[j])
            if m > maxM:
                maxM = m

    print(maxM)

part2()
