from common.io import readfile

def turn(heading, deg):
    assert deg in [90, 180, 270, -90, -180, -270], 'bad turn instruction: %s' % deg
    cw = ['N', 'E', 'S', 'W']
    i = cw.index(heading)
    newi = (i + (deg // 90)) % len(cw)
    return cw[newi]

def move(pos, heading, instruction):
    x, y = pos
    op, arg = instruction
    match op:
        case 'N':
            return ((x, y + arg), heading)
        case 'S':
            return ((x, y - arg), heading)
        case 'E':
            return ((x + arg, y), heading)
        case 'W':
            return ((x - arg, y), heading)
        case 'L':
            return (pos, turn(heading, -arg))
        case 'R':
            return (pos, turn(heading, arg))
        case 'F':
            return move(pos, heading, (heading, arg))

def rotate(wpos, deg):
    assert deg in [90, 180, 270], 'bad rotate instruction: %s' % deg
    wx, wy = wpos
    match deg:
       case 90:
           return (wy, -wx)
       case 180:
           return (-wx, -wy)
       case 270:
           return (-wy, wx)

def move2(pos, wpos, instruction):
    x, y = pos
    wx, wy = wpos
    op, arg = instruction
    match op:
        case 'N':
            return (pos, (wx, wy + arg))
        case 'S':
            return (pos, (wx, wy - arg))
        case 'E':
            return (pos, (wx + arg, wy))
        case 'W':
            return (pos, (wx - arg, wy))
        case 'L':
            return (pos, rotate(wpos, 360 - arg))
        case 'R':
            return (pos, rotate(wpos, arg))
        case 'F':
            return ((x + arg * wx, y + arg * wy), wpos)

def part1():
    instructions = []
    for line in readfile('day12.txt'):
        instructions.append((line[0], int(line[1:])))

    print(instructions)
    pos = (0, 0)
    heading = 'E'
    for inst in instructions:
        pos, heading = move(pos, heading, inst)
    print(pos, heading)
    print(abs(pos[0]) + abs(pos[1]))

def part2():
    instructions = []
    for line in readfile('day12.txt'):
        instructions.append((line[0], int(line[1:])))

    pos = (0, 0)
    wpos = (10, 1)
    for inst in instructions:
        pos, wpos = move2(pos, wpos, inst)
    print(pos, wpos)
    print(abs(pos[0]) + abs(pos[1]))

part2()
