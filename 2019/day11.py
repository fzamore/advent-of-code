from enum import IntEnum

from common.sparsegrid import SparseGrid

input = open('day11.txt').read().split(',')

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

def updateHeading(heading: tuple[int, int], *, leftTurn: bool) -> tuple[int, int]:
  match heading:
    case (0, -1): # up
      return (-1, 0) if leftTurn else (1, 0)
    case (-1, 0): # left
      return (0, 1) if leftTurn else (0, -1)
    case (0, 1): # down
      return (1, 0) if leftTurn else (-1, 0)
    case (1, 0): # right
      return (0, -1) if leftTurn else (0, 1)
    case _:
      assert False, 'invalid heading: %s' % str(heading)

def runMachine(
  memory: dict[int, int],
  grid: SparseGrid,
  initialPos: tuple[int, int],
) -> None:
  px, py = initialPos
  heading = (0, -1)
  outputCount = 0
  pc = 0
  relativeBase = 0
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
        inputValue = grid.getValue((px, py), 0)
        print('input inst at:', pc, inputValue)
        memory[dst] = inputValue
        pc += Op.getParamCount(opcode) + 1
      case Op.OUTPUT:
        output = paramValues[0]
        print('OUTPUT:', output)
        pc += Op.getParamCount(opcode) + 1
        if outputCount % 2 == 0:
          grid.setValue((px, py), output)
        else:
          heading = updateHeading(heading, leftTurn=(output == 0))
          px, py = px + heading[0], py + heading[1]
        outputCount += 1
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

def part1() -> None:
  memory = dict(zip(range(len(input)), list(map(int, input))))
  grid = SparseGrid(2)
  runMachine(memory, grid, (0, 0))
  print(len(grid.getAllCoords()))

def part2() -> None:
  memory = dict(zip(range(len(input)), list(map(int, input))))
  grid = SparseGrid(2)
  grid.setValue((0, 0), 1)
  runMachine(memory, grid, (0, 0))
  grid.print2D(default=' ', charMap = {1: '#', 0: ' '})

part2()
