from common.shortestpath import dijkstra
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
    s = \
        positions['A1'] + ',' + \
        positions['A2'] + ',' + \
        positions['B1'] + ',' + \
        positions['B2'] + ',' + \
        positions['C1'] + ',' + \
        positions['C2'] + ',' + \
        positions['D1'] + ',' + \
        positions['D2']

    if 'A3' in positions:
        s += ',' + \
             positions['A3'] + ',' + \
             positions['A4'] + ',' + \
             positions['B3'] + ',' + \
             positions['B4'] + ',' + \
             positions['C3'] + ',' + \
             positions['C4'] + ',' + \
             positions['D3'] + ',' + \
             positions['D4']
    return s

def deserialize(s):
    v = s.split(',')
    assert len(v) == 8 or len(v) == 16, 'bad serialization: %s' % s
    d = {
        'A1': v[0],
        'A2': v[1],
        'B1': v[2],
        'B2': v[3],
        'C1': v[4],
        'C2': v[5],
        'D1': v[6],
        'D2': v[7],
    }
    if len(v) == 16:
        d['A3'] = v[8]
        d['A4'] = v[9]
        d['B3'] = v[10]
        d['B4'] = v[11]
        d['C3'] = v[12]
        d['C4'] = v[13]
        d['D3'] = v[14]
        d['D4'] = v[15]
    return d

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
    backCell = 4 if ('a4', 'd4') in moveMap else 2

    # try room cells from back to front
    for r in range(backCell, 0, -1):
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

def moveIntoCaves(positions, moveMap):
    # initialize with the start state
    startNode = serialize(positions)

    def getAdjacentNodes(node):
        curPositions = deserialize(node)
        #printCave(curPositions)
        reversePositions = {v: k for k, v in curPositions.items()}
        for nextPositions, delta in getNextPositions(curPositions, reversePositions, moveMap):
            yield (serialize(nextPositions), delta)

    def isDestNode(node):
        return isDone(deserialize(node))

    return dijkstra(startNode, getAdjacentNodes, isDestNode)

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

    rooms = ['a', 'b', 'c', 'd']

    # line 1
    print('###', end='')
    for r in rooms:
        print(reversePositions['%s1' % r][0], end='')
        print('#', end='')
    print('##')

    # line 2
    print('  #', end='')
    for r in rooms:
        print(reversePositions['%s2' % r][0], end='')
        print('#', end='')
    print()

    if 'a3' in reversePositions:
        # line 3
        print('  #', end='')
        for r in rooms:
            print(reversePositions['%s3' % r][0], end='')
            print('#', end='')
        print()

        # line 4
        print('  #', end='')
        for r in rooms:
            print(reversePositions['%s4' % r][0], end='')
            print('#', end='')
        print()

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
    positionsS, score = moveIntoCaves(positions, moveMap)
    print('done. final position:')
    printCave(deserialize(positionsS))
    print(score)

def part2():
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
            positions[amph] = caveMap[i] + '4'

    # add part 2 input
    #D#C#B#A#
    #D#B#A#C#
    positions['D3'] = 'a2'
    positions['D4'] = 'a3'
    positions['C3'] = 'b2'
    positions['B3'] = 'b3'
    positions['B4'] = 'c2'
    positions['A3'] = 'c3'
    positions['A4'] = 'd2'
    positions['C4'] = 'd3'

    print('initial position:')
    printCave(positions)

    moveMap = makeMoveMap()

    # add new entries to movemap
    for r in ['a', 'b', 'c', 'd']:
        room1Cell = '%s1' % r
        room2Cell = '%s2' % r
        room3Cell = '%s3' % r
        room4Cell = '%s4' % r
        # add moves from room to hallway and vice-versa
        for h in [0, 1, 3, 5, 7, 9, 10]:
            hallwayCell = 'h%d' % h
            room2moves = moveMap[(room2Cell, hallwayCell)]
            hallwayMoves = moveMap[(hallwayCell, room2Cell)]

            moveMap[(room3Cell, hallwayCell)] = [room2Cell] + room2moves
            moveMap[(hallwayCell, room3Cell)] = hallwayMoves + [room3Cell]

            moveMap[(room4Cell, hallwayCell)] = [room3Cell, room2Cell] + room2moves
            moveMap[(hallwayCell, room4Cell)] = hallwayMoves + [room3Cell, room4Cell]

        # add room-to-room moves
        for otherR in ['a', 'b', 'c', 'd']:
            if r == otherR:
                continue

            otherRoom1Cell = '%s1' % otherR
            otherRoom2Cell = '%s2' % otherR
            otherRoom3Cell = '%s3' % otherR
            otherRoom4Cell = '%s4' % otherR

            roomToRoomMoves = [room1Cell] + moveMap[(room1Cell, otherRoom1Cell)]

            moveMap[(room3Cell, otherRoom1Cell)] = [room2Cell] + roomToRoomMoves
            moveMap[(room4Cell, otherRoom1Cell)] = [room3Cell, room2Cell] + roomToRoomMoves
            moveMap[(room3Cell, otherRoom2Cell)] = [room2Cell] + roomToRoomMoves + [otherRoom2Cell]
            moveMap[(room4Cell, otherRoom2Cell)] = [room3Cell, room2Cell] + roomToRoomMoves + [otherRoom2Cell]
            moveMap[(room3Cell, otherRoom3Cell)] = moveMap[(room3Cell, otherRoom2Cell)] + [otherRoom3Cell]
            moveMap[(room4Cell, otherRoom3Cell)] = moveMap[(room4Cell, otherRoom2Cell)] + [otherRoom3Cell]
            moveMap[(room3Cell, otherRoom4Cell)] = moveMap[(room3Cell, otherRoom3Cell)] + [otherRoom4Cell]
            moveMap[(room4Cell, otherRoom4Cell)] = moveMap[(room4Cell, otherRoom3Cell)] + [otherRoom4Cell]

    #for cell in moveMap:
    #   print(cell, ':', moveMap[cell])
    print('movemap entries:', len(moveMap))

    print('moving...')
    positionsS, score = moveIntoCaves(positions, moveMap)
    print('done. final position:')
    printCave(deserialize(positionsS))
    print(score)

part2()
