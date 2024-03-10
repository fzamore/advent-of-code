from enum import IntEnum

input = open('day19.txt').read().split(',')

class Op(IntEnum):
  ADD: int = 1
  MUL: int = 2
  INPUT: int = 3
  OUTPUT: int = 4
  JUMP_IF_TRUE: int = 5
  JUMP_IF_FALSE: int = 6
  LESS_THAN: int = 7
  EQUALS: int = 8
  RELATIVE_BASE: int = 9

  @staticmethod
  def getParamCount(op: int) -> int:
    return {
      Op.ADD: 3,
      Op.MUL: 3,
      Op.INPUT: 1,
      Op.OUTPUT: 1,
      Op.JUMP_IF_TRUE: 2,
      Op.JUMP_IF_FALSE: 2,
      Op.LESS_THAN: 3,
      Op.EQUALS: 3,
      Op.RELATIVE_BASE: 1,
   }[Op(op)]

def getParameterAddresses(memory: dict[int, int], pc: int, relativeBase: int) -> list[int]:
  value = memory[pc]
  opcode = value % 100
  paramModes = str(value // 100)[::-1] + '000' # tack on extra zeroes, which is the default
  results = []
  for i in range(Op.getParamCount(opcode)):
    mode = paramModes[i]
    match mode:
      case '0':
        address = memory.get(pc + i + 1, 0)
      case '1':
        address = pc + i + 1
      case '2':
        address = memory.get(pc + i + 1, 0) + relativeBase
      case _:
        assert False, 'bad mode: %s' % mode
    results.append(address)
  assert len(results) <= 3, 'bad addresses: %s' % results
  return results

def runMachine(memory: dict[int, int], inputs: list[int]) -> list[int]:
  pc = 0
  relativeBase = 0
  outputs = []
  while (value := memory[pc]) != 99:
    opcode = value % 100
    paramAddresses = getParameterAddresses(memory, pc, relativeBase)
    paramValues = [memory.get(x, 0) for x in paramAddresses]
    assert len(paramValues) == Op.getParamCount(opcode), \
      'bad paramValues for opcode: %d, %s' % (opcode, paramValues)

    # Asssume the destination is the last parameter, if it exists.
    dst = paramAddresses[-1]
    assert dst >= 0, 'dst cannot be negative'

    match opcode:
      case Op.ADD:
        memory[dst] = paramValues[0] + paramValues[1]
        pc += Op.getParamCount(opcode) + 1
      case Op.MUL:
        memory[dst] = paramValues[0] * paramValues[1]
        pc += Op.getParamCount(opcode) + 1
      case Op.INPUT:
        assert dst >= 0, 'dst cannot be negative'
        memory[dst] = inputs.pop(0)
        pc += Op.getParamCount(opcode) + 1
      case Op.OUTPUT:
        pc += Op.getParamCount(opcode) + 1
        outputs.append(paramValues[0])
      case Op.JUMP_IF_TRUE:
        if paramValues[0] != 0:
          pc = paramValues[1]
        else:
          pc += Op.getParamCount(opcode) + 1
      case Op.JUMP_IF_FALSE:
        if paramValues[0] == 0:
          pc = paramValues[1]
        else:
          pc += Op.getParamCount(opcode) + 1
      case Op.LESS_THAN:
        memory[dst] = 1 if paramValues[0] < paramValues[1] else 0
        pc += Op.getParamCount(opcode) + 1
      case Op.EQUALS:
        memory[dst] = 1 if paramValues[0] == paramValues[1] else 0
        pc += Op.getParamCount(opcode) + 1
      case Op.RELATIVE_BASE:
        relativeBase += paramValues[0]
        pc += Op.getParamCount(opcode) + 1
      case _:
        assert False, 'bad opcode: %s' % opcode

  return outputs

def inBeam(x: int, y: int) -> bool:
  memory = dict(zip(range(len(input)), list(map(int, input))))
  return runMachine(memory, [x, y])[0] == 1

def part1() -> None:
  memory = dict(zip(range(len(input)), list(map(int, input))))
  result = 0
  for x in range(50):
    for y in range(50):
      outputs = runMachine(memory.copy(), [x, y])
      assert len(outputs) == 1, 'bad output'
      result += outputs[0]
  print(result)

def part2() -> None:
  start = 7, 9 # found by printing out the tractor beam pattern
  print('start:', start)
  sx, sy = start
  rows = {sy: sx}
  row = sy
  size = 100

  # For each row, calculate the max column within the beam.
  while True:
    mx = rows[row]
    row += 1

    newMax = mx
    while inBeam(newMax, row):
      newMax += 1
    # We went beyond the beam, so course-correct by 1.
    newMax -= 1

    rows[row] = newMax

    # Assume this coordinate is the top right of the square. If the bottom
    # left of the correctly-sized square is also in the beam, then we have
    # our answer.
    newRow = row + size - 1
    newCol = newMax - size + 1
    if inBeam(newCol, newRow):
      print('done:', newCol, row)
      print(10000 * newCol + row)
      break

part2()
