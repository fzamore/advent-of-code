from heapq import heappush, heappop
from collections import defaultdict
from copy import deepcopy

# map from (cell1, cell2) => path from cell1 to cell2
def makeMoveMap():
    hallway = ['h%d' % x for x in range(0, 11)]
    doorways = {
        'a': 2,
        'b': 4,
        'c': 6,
        'd': 8,
    }

    moveMap = {}

    for room in doorways:
        room1 = '%s1' % room
        room2 = '%s2' % room
        doorway = doorways[room]
        doorwayCell = 'h%d' % doorway

        # moving left in the hallway
        for h in range(doorway - 1, -1, -1):
            if h in [2, 4, 6, 8]:
                continue
            hallwayCell = 'h%d' % h
            moveMap[(room1, hallwayCell)] = ['h%d' % x for x in range(doorway, h, -1)]
            moveMap[(room2, hallwayCell)] = [room1] + moveMap[(room1, hallwayCell)]

        # moving right in the hallway
        for h in range(doorway + 1, 11):
            if h in [2, 4, 6, 8]:
                continue
            hallwayCell = 'h%d' % h
            moveMap[(room1, hallwayCell)] = ['h%d' % x for x in range(doorway, h)]
            moveMap[(room2, hallwayCell)] = [room1] + moveMap[(room1, hallwayCell)]

    # add the reverse of each room->hallway path
    moveMapCopy = deepcopy(moveMap)
    for cell1, cell2 in moveMapCopy:
        path = moveMapCopy[(cell1, cell2)]
        path.reverse()
        moveMap[(cell2, cell1)] = path

    # room to room paths
    for room in doorways:
        for otherRoom in doorways:
            if room == otherRoom:
                continue
            doorway = doorways[room]
            otherDoorway = doorways[otherRoom]
            room1Cell = '%s1' % room
            room2Cell = '%s2' % room
            otherRoom1Cell = '%s1' % otherRoom
            otherRoom2Cell = '%s2' % otherRoom
            doorwayCell = 'h%d' % doorway
            otherDoorwayCell = 'h%d' % otherDoorway

            assert otherDoorway != doorway, 'bad room iteration, %d %d' % (otherDoorway, doorway)

            if otherDoorway <= doorway:
                continue

            path = ['h%d' % x for x in range(doorway, otherDoorway + 1)]
            moveMap[(room1Cell, otherRoom1Cell)] = path
            moveMap[(room1Cell, otherRoom2Cell)] = path + [otherRoom1Cell]
            moveMap[(room2Cell, otherRoom1Cell)] = [room1Cell] + path
            moveMap[(room2Cell, otherRoom2Cell)] = [room1Cell] + path + [otherRoom1Cell]

            # reverse paths
            moveMap[(otherRoom1Cell, room1Cell)] = moveMap[(room1Cell, otherRoom1Cell)][::-1]
            moveMap[(otherRoom1Cell, room2Cell)] = moveMap[(room2Cell, otherRoom1Cell)][::-1]
            moveMap[(otherRoom2Cell, room1Cell)] = moveMap[(room1Cell, otherRoom2Cell)][::-1]
            moveMap[(otherRoom2Cell, room2Cell)] = moveMap[(room2Cell, otherRoom2Cell)][::-1]

    # add destination to each entry in map
    for cell1, cell2 in moveMap:
        moveMap[(cell1, cell2)] += [cell2]

    return moveMap

def serialize(positions):
    return \
        positions['A1'] + ',' + \
        positions['A2'] + ',' + \
        positions['B1'] + ',' + \
        positions['B2'] + ',' + \
        positions['C1'] + ',' + \
        positions['C2'] + ',' + \
        positions['D1'] + ',' + \
        positions['D2']

def deserialize(s):
    v = s.split(',')
    assert len(v) == 8, 'bad serialization: %s' % s
    return {
        'A1': v[0],
        'A2': v[1],
        'B1': v[2],
        'B2': v[3],
        'C1': v[4],
        'C2': v[5],
        'D1': v[6],
        'D2': v[7],
    }

def isDone(positions):
    for amph in positions:
        if amph[0].lower() != positions[amph][0]:
            return False
    return True

def isCellOccupied(reversePositions, cell):
    return cell in reversePositions

def isPathClear(reversePositions, path):
    for cell in path:
        if isCellOccupied(reversePositions, cell):
            return False
    return True

def tryEnterRoom(amph, amphCell, reversePositions, moveMap):
    # try room cells from back to front
    for r in range(2, 0, -1):
        roomCell = amph[0].lower() + str(r)
        if isCellOccupied(reversePositions, roomCell):
            if reversePositions[roomCell][0] != amph[0]:
                # if there's an amphipod of a differing type in this room, we can't enter
                return None
            # otherwise, there's an amphipod of the same type in the
            # cell, so keep checking other cells in the room
            continue

        if isPathClear(reversePositions, moveMap[(amphCell, roomCell)]):
            # the path to this cell is clear. move into it
            return roomCell

    return None

def getNextPositions(positions, reversePositions, moveMap):
    weights = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }

    result = []

    for amph in positions:
        amphCell = positions[amph]
        inHallway = amphCell[0] == 'h'

        weight = weights[amph[0]]

        if inHallway:
            # if any amphipod can enter home, that should be the next move
            roomCell = tryEnterRoom(amph, amphCell, reversePositions, moveMap)
            if roomCell:
                curNextPositions = deepcopy(positions)
                curNextPositions[amph] = roomCell
                score = weight * len(moveMap[(amphCell, roomCell)])
                return [(curNextPositions, score)]

            # otherwise, if we're already in the hallway, we can't move
            continue

        # otherwise, iterate through all possible moves into the hallway
        for destCell in ['h0', 'h1', 'h3', 'h5', 'h7', 'h9', 'h10']:
            path = moveMap[(amphCell, destCell)]

            if not isPathClear(reversePositions, path):
                continue

            # move into the new cell
            curNextPositions = deepcopy(positions)
            curNextPositions[amph] = destCell
            score = weight * len(path)
            result.append((curNextPositions, score))

    # return (nextPositions, delta) tuples
    return result

def dijkstra(positions, moveMap):
    # min-heap priority queue of position-states with energy as key
    q = []

    # map from state to energy consumed to get to that state
    d = defaultdict(lambda: float('inf'))

    # initialize with the start state
    s = serialize(positions)
    heappush(q, (0, s))
    d[s] = 0

    while len(q) > 0:
        curS = heappop(q)[1]
        curPositions = deserialize(curS)

        #printCave(curPositions)

        score = d[curS]
        assert d[curS] != float('inf'), 'Missing point in dict: %s' % curS

        if isDone(curPositions):
            # done
            return (score, curPositions)

        reversePositions = {v: k for k, v in curPositions.items()}
        for nextPositions, delta in getNextPositions(curPositions, reversePositions, moveMap):
            nextS = serialize(nextPositions)
            newScore = score + delta
            if newScore < d[nextS]:
                # We've improved the energy requried to get to this state. Update the queue
                # and distance map. We don't need to modify its existing entry
                # in the priority queue (if it exists) because the new entry
                # will always be lower, and thus will be popped off the queue
                # before the existing entry.
                d[nextS] = newScore
                heappush(q, (newScore, nextS))

    assert False, 'did not find shortest path'

def printCave(positions):
    reversePositions = {v: k for k, v in positions.items()}
    for cell in ['a1', 'a2', 'b1', 'b2', 'c1', 'c2', 'd1', 'd2']:
        if cell not in reversePositions:
            reversePositions[cell] = '..'

    # top
    print('#############')

    # hallway
    print('#', end='')
    for i in range(0, 11):
        cell = 'h%d' % i
        if cell in reversePositions:
            print(reversePositions[cell][0], end='')
        else:
            print('.', end='')
    print('#')

    # line 1
    print('###', end='')
    print(reversePositions['a1'][0], end='')
    print('#', end='')
    print(reversePositions['b1'][0], end='')
    print('#', end='')
    print(reversePositions['c1'][0], end='')
    print('#', end='')
    print(reversePositions['d1'][0], end='')
    print('###')

    # line 2
    print('  #', end='')
    print(reversePositions['a2'][0], end='')
    print('#', end='')
    print(reversePositions['b2'][0], end='')
    print('#', end='')
    print(reversePositions['c2'][0], end='')
    print('#', end='')
    print(reversePositions['d2'][0], end='')
    print('#')

    # bottom
    print('  #########  ')
    print()

def part1():
    positions = {}

    with open('day23.txt') as f:
        caveMap = {
            3: 'a',
            5: 'b',
            7: 'c',
            9: 'd',
        }
        seenValues = set()

        f.readline()
        f.readline()
        line1 = f.readline()
        for i in caveMap:
            v = line1[i]
            amph = v + '1'
            amph = v + '2' if amph in seenValues else amph
            seenValues.add(amph)
            positions[amph] = caveMap[i] + '1'

        line2 = f.readline()
        for i in caveMap:
            v = line2[i]
            amph = v + '1'
            amph = v + '2' if amph in seenValues else amph
            seenValues.add(amph)
            positions[amph] = caveMap[i] + '2'

    print('initial position:')
    printCave(positions)

    moveMap = makeMoveMap()
    print('movemap entries:', len(moveMap))
    #for cell in moveMap:
    #   print(cell, ':', moveMap[cell])

    print('moving...')
    score, positions = dijkstra(positions, moveMap)
    print('done. final position:')
    printCave(positions)
    print(score)

part1()
