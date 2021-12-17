def isPosPastTargetArea(pos, targetArea):
    if isPosInTargetArea(pos, targetArea):
        return False

    px, py = pos
    taStart, taEnd = targetArea
    return px > taEnd[0] or py < taStart[1]

def isPosInTargetArea(pos, targetArea):
    px, py = pos
    taStart, taEnd = targetArea

    if px < taStart[0] or px > taEnd[0]:
        return False
    if py < taStart[1] or py > taEnd[1]:
        return False
    return True

def fireProbe(v0, targetArea, n=1000):
    pos = (0, 0)
    positions = [pos]
    v = v0
    for i in range(n):
        #print(i, pos, v)

        pos = (pos[0] + v[0], pos[1] + v[1])
        positions.append(pos)

        if v[0] < 0:
            vx = v[0] + 1
        elif v[0] > 0:
            vx = v[0] - 1
        else:
            vx = v[0]
        vy = v[1] - 1
        v = (vx, vy)

        if isPosInTargetArea(pos, targetArea):
            return (True, positions)

        if isPosPastTargetArea(pos, targetArea):
            return (False, positions)

    print(
        'did not make it, v0: %s, lastPos: %s positionsCount: %d' % \
        (str(v0), str(positions[-1]), len(positions)),
    )
    return False, positions

'''
p_n = n * v_0 - (n - 1) * n / 2
v_n = v_0 - n

After vx_0 steps, the x coord doesn't change
'''

def part1():
    with open('day17.txt') as f:
        line = f.readline().strip()
        coordsInfo = line[13:].split(', ')
        xCoords = coordsInfo[0][2:].split('..')
        yCoords = coordsInfo[1][2:].split('..')

        targetArea = [
            (int(xCoords[0]), int(yCoords[0])),
            (int(xCoords[1]), int(yCoords[1])),
        ]

        assert \
            targetArea[0][0] < targetArea[1][0] and \
            targetArea[0][1] < targetArea[1][1], \
            'Bad target area: %s' % (str(targetArea))

    print('target area:', targetArea)

    maxY = -float('inf')
    for x in range(1, 500):
        for y in range(1, 500):
            didHit, positions = fireProbe((x, y), targetArea)
            if didHit:
                maxYPos = max([x[1] for x in positions])
                if maxYPos > maxY:
                    maxY = maxYPos

    print(maxY)

    #didHitTarget, positions = fireProbe((17, -4), targetArea)
    #print(didHitTarget, positions[-1], len(positions))

def part2():
    with open('day17.txt') as f:
        line = f.readline().strip()
        coordsInfo = line[13:].split(', ')
        xCoords = coordsInfo[0][2:].split('..')
        yCoords = coordsInfo[1][2:].split('..')

        targetArea = [
            (int(xCoords[0]), int(yCoords[0])),
            (int(xCoords[1]), int(yCoords[1])),
        ]

        assert \
            targetArea[0][0] < targetArea[1][0] and \
            targetArea[0][1] < targetArea[1][1], \
            'Bad target area: %s' % (str(targetArea))

    print('target area:', targetArea)

    count = 0
    for x in range(1, 500):
        for y in range(-500, 500):
            didHit, positions = fireProbe((x, y), targetArea)
            if didHit:
                count += 1

    print(count)

part2()
