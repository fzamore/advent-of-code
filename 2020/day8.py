from common.io import readfile

def execute(instructions):
    executed = set()
    acc = 0
    i = 0
    while i < len(instructions):
        if i in executed:
            return acc, i
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

    return acc, i - 1

def part1():
    instructions = []
    for line in readfile('day8.txt'):
        op = line[0:3]
        arg = int(line[4:])
        instructions.append((op, arg))

    val, _ = execute(instructions)
    print(val)

def part2():
    instructions = []
    for line in readfile('day8.txt'):
        op = line[0:3]
        arg = int(line[4:])
        instructions.append((op, arg))

    print('instruction count', len(instructions))
    for i in range(0, len(instructions)):
        op, arg = instructions[i]
        if op == 'acc':
            continue
        instructions[i] = (
            'jmp' if op == 'nop' else 'nop',
            arg,
        )
        val, last = execute(instructions)
        if last == len(instructions) - 1:
            print('result', val)
            break
        # swap instruction back
        instructions[i] = (
            'jmp' if op == 'jmp' else 'nop',
            arg,
        )

part2()
