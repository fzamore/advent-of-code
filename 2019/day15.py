from enum import IntEnum
from common.sparsegrid import SparseGrid
from collections import deque

input = open('day15.txt').read().split(',')

Coords = tuple[int, int]

class Dir(IntEnum):
  NORTH: int = 1
  SOUTH: int = 2
  WEST: int = 3
  EAST: int = 4

  @staticmethod
  def getDelta(dir: 'Dir') -> tuple[int, int]:
    return {
      Dir.NORTH: (0, -1),
      Dir.SOUTH: (0, 1),
      Dir.WEST: (-1, 0),
      Dir.EAST: (1, 0),
    }[dir]

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

def runMachine(memory: dict[int, int], input: int) -> int:
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
        memory[dst] = input
        pc += Op.getParamCount(opcode) + 1
      case Op.OUTPUT:
        pc += Op.getParamCount(opcode) + 1
        return paramValues[0]
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

  assert False, 'should have returned a value'

def getAdjacentPosition(pos: Coords, dir: Dir):
  x, y = pos
  dx, dy = Dir.getDelta(dir)
  npos = x + dx, y + dy
  assert npos != pos
  return npos

def bfs(grid: SparseGrid, initialMemory: dict[int, int]) -> tuple[Coords, int]:
  start = (0, 0)
  seen = {start}
  grid.setValue(start, 'S')
  q: deque = deque()
  q.append((0, start, initialMemory.copy()))
  result = None
  while len(q) > 0:
    steps, pos, memory = q.popleft()
    for dir in Dir:
      npos = getAdjacentPosition(pos, dir)
      if npos in seen:
        continue

      mem = memory.copy()
      output = runMachine(mem, dir)
      values = ['#', '.', 'E']
      grid.setValue(npos, values[output])
      seen.add(npos)

      if output != 0:
        q.append((steps + 1, npos, mem))

        if output == 2:
          result = (npos, steps + 1)

  assert result is not None, 'did not find end'
  return result

def bfs2(grid: SparseGrid, start: Coords) -> int:
  deltas = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
  ]
  minutes = 0
  q: deque = deque()
  seen = {start}
  q.append((0, start))
  while len(q) > 0:
    steps, (x, y) = q.popleft()
    minutes = max(minutes, steps)
    for dx, dy in deltas:
      npos = (x + dx, y + dy)
      if npos in seen:
        continue
      seen.add(npos)

      v = grid.getValue(npos)
      assert v is not None, 'traverse to bad grid cell'
      if v != '#':
        q.append((steps + 1, npos))

  return minutes

def part1() -> None:
  memory = dict(zip(range(len(input)), list(map(int, input))))

  grid = SparseGrid(2)
  result = bfs(grid, memory)
  grid.print2D(default='*')
  print(result[1])

def part2() -> None:
  memory = dict(zip(range(len(input)), list(map(int, input))))

  grid = SparseGrid(2)
  result = bfs(grid, memory)
  grid.print2D(default='*')
  start = result[0]
  print('end:', start)

  print(bfs2(grid, start))

part2()
