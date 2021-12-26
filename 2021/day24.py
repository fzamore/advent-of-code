def isValidRegister(r):
    match r:
      case 'w':
        return True
      case 'x':
        return True
      case 'y':
        return True
      case 'z':
        return True
      case _:
        return False

def validateRegister(r):
    assert isValidRegister(r), 'invalid register: %s' % r
    return r

def getValue(x, registers):
    if isValidRegister(x):
        return int(registers[x])
    return int(x)

def printRegisters(registers):
    print()
    print('Registers:')
    for r in ['w', 'x', 'y', 'z']:
        print('%s: %d' % (r, registers[r]))
    print()

def printRegistersShort(registers):
    for r in ['w', 'x', 'y', 'z']:
        print('%d ' % registers[r], end='')
    print()

def executeInstructions(instructions, registers, inputs={}):
    i = 0
    for instruction in instructions:
      op = instruction[0]
      v1 = instruction[1]
      v2 = getValue(instruction[2], registers) if len(instruction) == 3 else None
      r = registers

      match op:
        case 'inp':
          if i in inputs:
              inputValue = inputs[i]
          else:
              printRegisters(registers)
              inputValue = input('Input (%s, %d): ' % (v1, i + 1))
          r[v1] = int(inputValue)
          i += 1
        case 'add':
          r[v1] = r[v1] + v2
        case 'mul':
          r[v1] = r[v1] * v2
        case 'div':
          assert v2 != 0, 'div by zero'
          if r[v1] < 0:
              print('WARNING: negative division: %d %d' % (r[v1], v2))
          r[v1] = r[v1] // v2
        case 'mod':
          assert r[v1] >= 0 and v2 > 0, 'bad mod: %d, %d' % (r[v1], v2)
          r[v1] = r[v1] % v2
        case 'eql':
          r[v1] = 1 if r[v1] == v2 else 0
        case _:
          assert False, 'bad instruction %s' % instruction

      #printRegistersShort(registers)

def doesMatchEndRegisters(registers, endRegisters):
    for r in endRegisters:
        if registers[r] != endRegisters[r]:
            return False
    return True

# executes a single input block in reverse, such that the z result is destZ
def executeSingleBlockBackward(constants, i, w, destZ):
    # return possible values of z that could've led to destZ
    a = constants['a'][i]
    b = constants['b'][i]
    c = constants['c'][i]

    # need to solve for z in the following equations. all other values are known
    match a:
        case 1:
            # these input blocks cause z to increase, so reversing them causes z to decrease
            # destZ = 26 * (z // a) + w + c
            numerator = destZ - w - c
            if numerator % 26 != 0:
                # discard non-integer results of division
                return None
            z = numerator // 26
            if z % 26 != w - b:
                # assume the branch condition failed
                return z
        case 26:
            # these input blocks cause z to decrease, so reversing them causes z to increase
            # destZ = z // 26
            # reversing integer division is tricky
            # given A = B // C, then to solve for B, do:
            #   B = A * C + [0, C - 1]
            # for all  integer values in the range [0, C - 1]

            # find possible values of z
            for k in range(0, 26):
                z = destZ * 26 + k
                if z % 26 == w - b:
                    # assume the branch condition succeeded
                    return z

        case _:
            assert False, 'bad a-value' % (a, i)

    return None

# executes the entire instruction set in reverse
def executeBackward(constants, wStr, i, wRange, destZs): # todo: change destZs to singleton?
    if len(destZs) > 1:
        print('whoa whoa', destZs)
        return

    newZs = []
    for w in wRange:
        for destZ in destZs:
            newZ = executeSingleBlockBackward(constants, i, w, destZ)
            if newZ != None:
                newZs.append((w, newZ))

    result = []
    for w, newZ in newZs:
        newWStr = str(w) + wStr
        if i == 0:
            result.append(newWStr)
        else:
            subResults = executeBackward(constants, newWStr, i - 1, wRange, [newZ])
            result.extend(subResults)
    return result

# this was used to print diffs of input blocks, to get a, b, and c values
def printInputBlockDiffs(inputBlocks):
    differingInstructions = set()
    for i in range(1, len(inputBlocks)):
        if len(inputBlocks[i]) != len(inputBlocks[0]):
            print('different lengths')
        for j in range(0, len(inputBlocks[i])):
            if inputBlocks[i][j] != inputBlocks[0][j]:
                differingInstructions.add(j)

    for i in differingInstructions:
        print()
        print(i)
        for j in range(0, len(inputBlocks)):
            print(j + 1, inputBlocks[j][i])
        print()

def parseInput(filename):
    instructions = []
    with open(filename) as f:
        for line in f.read().splitlines():
            values = line.split()
            assert len(values) == 2 or len(values) == 3, 'bad input line: %s' % line
            op = values[0]
            v1 = validateRegister(values[1])
            if len(values) == 2:
                assert op == 'inp', 'line only has 2 values: %s' % line
                inst = (op, v1)
            else:
                v2 = values[2]
                if not isValidRegister(v2):
                    v2 = int(v2)
                inst = (op, v1, v2)
            instructions.append(inst)
    return instructions

def part1():
    instructions = parseInput('day24.txt')
    registers = {
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0,
    }
    wStr = '29991993698469'
    inputs = {}
    if wStr != None:
        for i in range(0, len(wStr)):
            inputs[i] = wStr[i]
    executeInstructions(instructions, registers, inputs)
    printRegisters(registers)

    '''
    inputBlocks = []
    inputBlock = []
    for inst in instructions:
        if inst[0] == 'inp' and len(inputBlock) != 0:
            inputBlocks.append(inputBlock)
            inputBlock = []
        inputBlock.append(inst)
    inputBlocks.append(inputBlock)

    print('input blocks:', len(inputBlocks))
    printInputBlockDiffs(inputBlocks)
    return
    '''

    # solve the problem
    constants = {
        'a': [1, 1, 1, 1, 26, 1, 1, 26, 1, 26, 26, 26, 26, 26],
        'b': [15, 11, 10, 12, -11, 11, 14, -6, 10, -6, -6, -16, -4, -2],
        'c': [9, 1, 11, 3, 10, 5, 0, 7, 9, 15, 4, 10, 4, 9],
    }

    # highest: 29991993698469
    # lowest: 14691271141118

    wRange = range(9, 0, -1) # part 1: find highest
    #wRange = range(1, 10) # part 2: find lowest
    result = executeBackward(constants, '', 13, wRange, [0])
    print('count', len(result))
    print(result[0])

part1()
