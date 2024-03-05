from enum import IntEnum
from common.sparsegrid import SparseGrid

input = open('day17.txt').read().split(',')

Coords = tuple[int, int]

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

def runMachine(memory: dict[int, int], inputs: list[int] = []) -> list[int]:
  outputs = []
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
        memory[dst] = inputs.pop(0)
        pc += Op.getParamCount(opcode) + 1
      case Op.OUTPUT:
        outputs.append(paramValues[0])
        pc += Op.getParamCount(opcode) + 1
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

def initMemory() -> dict[int, int]:
  return dict(zip(range(len(input)), list(map(int, input))))

def initGrid(memory: dict[int, int]) -> SparseGrid:
  outputs = runMachine(memory)
  print('outputs', len(outputs))

  grid = SparseGrid(2)
  x, y = 0, 0
  for c in outputs:
    if c == 10:
      x = 0
      y += 1
    else:
      grid.setValue((x, y), chr(c))
      x += 1
  return grid

def findStart(grid: SparseGrid) -> Coords:
  start = None
  for coords in grid.getAllCoords():
    if grid.getValue(coords) not in ['.', '#']:
      assert start is None, 'cannot be multiple start positions'
      start = coords
  assert start is not None, 'did not find start'
  assert len(start) == 2, 'bad coords'
  return start

def createPath(grid: SparseGrid) -> list[str | int]:
  start = findStart(grid)
  print('start:', start, grid.getValue(start))
  assert grid.getValue(start) == '^', 'assuming robot starts up for convention'

  x, y = start
  dx, dy = 1, 0
  distance = 0
  path: list[int | str] = ['R'] # Cheating by hardcoding first instruction.
  while True:
    nx, ny = x + dx, y + dy
    if grid.getValue((nx, ny)) != '#':
      path.append(distance)
      distance = 0
      # Need to turn 90 degrees.
      tdeltas = [(1, 0), (-1, 0)] if dx == 0 else [(0, 1), (0, -1)]
      for tdx, tdy in tdeltas:
        tx, ty = x + tdx, y + tdy
        if grid.getValue((tx, ty)) == '#':
          match tdx, tdy:
            case (1, 0): t = 'L' if dy == 1 else 'R'
            case (-1, 0): t = 'L' if dy == -1 else 'R'
            case (0, 1): t = 'L' if dx == -1 else 'R'
            case (0, -1): t = 'L' if dx == 1 else 'R'
            case _: assert False, 'bad turn deltas'

          dx, dy = tdx, tdy
          path.append(t)
      if path[-1] not in ['L', 'R']:
        # We needed to turn but couldn't. We must be at the end of the path.
        return path
    else:
      assert grid.getValue((nx, ny)) == '#', \
        'robot veered from scaffolding: (%d, %d): %s' % (nx, ny, path)
      distance += 1
      x, y = nx, ny

def funcToAscii(func: list) -> list[int]:
  result = []
  for e in func:
    # Multi-digit ints need to be broken up.
    for es in str(e):
      result.append(ord(es))
    result.append(ord(','))
  result = result[:-1] # remove the last comma
  result.append(ord('\n'))
  assert len(result) <= 20, 'ascii func too long'
  return result

def part1() -> None:
  memory = initMemory()
  grid = initGrid(memory)
  grid.print2D()

  w, h = grid.getMaxCoords()
  print('w x h:', w, h)

  intersections = []
  for x, y in grid.getAllCoords():
    isIntersection = True
    for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
      if grid.getValue((x + dx, y + dy), '.') != '#':
        isIntersection = False
        break
    if isIntersection:
      intersections.append((x, y))

  print('intersections:', len(intersections))
  print(sum([x * y for x, y in intersections]))

def part2() -> None:
  memory = initMemory()
  grid = initGrid(memory)
  grid.print2D()

  path = createPath(grid)
  print('path', len(path), path)

  # Determined by inspecting the path.
  funcs = {
    'A': ['R', 12, 'L', 8, 'R', 12],
    'B': ['R', 8, 'R', 6, 'R', 6, 'R', 8],
    'C': ['R', 8, 'L', 8, 'R', 8, 'R', 4, 'R', 4],
  }
  main = ['A', 'B', 'A', 'B', 'C', 'C', 'B', 'C', 'B', 'A']

  # Verify routines are correct.
  pi, mi = 0, 0
  while mi < len(main):
    func = funcs[main[mi]]
    for e in func:
      assert e == path[pi], 'func did not match path: %s' % str((mi, pi, main[mi], e))
      pi += 1
    mi += 1

  inputs = []
  inputs.extend(funcToAscii(main))
  inputs.extend(funcToAscii(funcs['A']))
  inputs.extend(funcToAscii(funcs['B']))
  inputs.extend(funcToAscii(funcs['C']))
  inputs.extend(funcToAscii(['n']))
  print('inputs', inputs)

  memory = initMemory()
  assert memory[0] == 1, 'bad value at address 0'
  memory[0] = 2 # wake up the robot
  outputs = runMachine(memory, inputs)
  print('outputs:', len(outputs))
  print(outputs[-1])

part2()
