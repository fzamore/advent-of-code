from common.io import readfile

def executeUntilLoop(instructions):
    executed = set()
    acc = 0
    i = 0
    while True:
        if i in executed:
            return acc
        executed.add(i)
        op, arg = instructions[i]
        match op:
            case 'acc':
                acc += arg
                i += 1
            case 'jmp':
                i += arg
            case 'nop':
                i += 1

def executeAndTryToTerminate(instructions, ic):
    op, arg = instructions[ic]
    if op == 'acc':
        # skip
        return None
    else:
        instructions[ic] = (
            'jmp' if op == 'nop' else 'nop',
            arg,
        )

    executed = set()
    acc = 0
    i = 0
    while i < len(instructions):
        if i in executed:
            return None
        executed.add(i)
        op, arg = instructions[i]
        match op:
            case 'acc':
                acc += arg
                i += 1
            case 'jmp':
                i += arg
            case 'nop':
                i += 1

    return acc

def part1():
    instructions = []
    for line in readfile('day8.txt'):
        op = line[0:3]
        arg = int(line[4:])
        instructions.append((op, arg))

    val = executeUntilLoop(instructions)
    print(val)

def part2():
    instructions = []
    for line in readfile('day8.txt'):
        op = line[0:3]
        arg = int(line[4:])
        instructions.append((op, arg))

    print('instruction count', len(instructions))
    for i in range(0, len(instructions)):
        val = executeAndTryToTerminate(instructions.copy(), i)
        if val == None:
            continue
        print('result', val)

part2()
