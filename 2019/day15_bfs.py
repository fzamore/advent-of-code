from enum import IntEnum
from typing import Optional
from common.sparsegrid import SparseGrid
from common.graphtraversal import bfs

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

def explore(grid: SparseGrid, initialMemory: dict[int, int]) -> tuple[Coords, int]:
  start = (0, 0)
  grid.setValue(start, 'S')
  end = None

  memories = {
    start: initialMemory,
  }

  def getAdjacentNodes(pos: Coords) -> list[Coords]:
    assert pos in memories, 'should have already run machine for node'
    memory = memories[pos]
    result = []
    for dir in Dir:
      npos = getAdjacentPosition(pos, dir)
      if npos not in memories:
        memCopy = memory.copy()
        output = runMachine(memCopy, dir)
        values = ['#', '.', 'E']
        grid.setValue(npos, values[output])
        memories[npos] = memCopy

        if output == 2:
          nonlocal end
          assert end is None, 'already found result'
          end = npos


      assert grid.hasValue(npos), 'should have already set value for pos'
      if grid.getValue(npos) != '#':
        # Include this node if it isn't a wall.
        result.append(npos)

    return result

  result = bfs(start, getAdjacentNodes)
  assert end is not None, 'did not find end'
  return (end, result[end])

def fillWithOxygen(grid: SparseGrid, start: Coords) -> int:
  def getAdjacentNodes(pos: Coords) -> list[Coords]:
    deltas = [
      (-1, 0),
      (1, 0),
      (0, -1),
      (0, 1),
    ]
    x, y = pos
    result = []
    for dx, dy in deltas:
      npos = (x + dx, y + dy)
      if grid.getValue(npos) != '#':
        result.append(npos)
    return result

  result = bfs(start, getAdjacentNodes)
  return max(result.values())

def part1() -> None:
  memory = dict(zip(range(len(input)), list(map(int, input))))

  grid = SparseGrid(2)
  result = explore(grid, memory)
  grid.print2D(default='*')
  print(result[1])

def part2() -> None:
  memory = dict(zip(range(len(input)), list(map(int, input))))

  grid = SparseGrid(2)
  result = explore(grid, memory)
  grid.print2D(default='*')
  start = result[0]
  print('end:', start)

  print(fillWithOxygen(grid, start))

part2()
