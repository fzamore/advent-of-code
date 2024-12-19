from enum import IntEnum
from typing import Optional
from common.sparsegrid import SparseGrid
from common.graphtraversal import bfs
from intcode import IntcodeVM

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


def getAdjacentPosition(pos: Coords, dir: Dir):
  x, y = pos
  dx, dy = Dir.getDelta(dir)
  npos = x + dx, y + dy
  assert npos != pos
  return npos

def explore(grid: SparseGrid, initialMachine: IntcodeVM) -> tuple[Coords, int]:
  start = (0, 0)
  grid.setValue(start, 'S')
  end = None

  machines = {
    start: initialMachine,
  }

  def getAdjacentNodes(pos: Coords) -> list[Coords]:
    assert pos in machines, 'should have already run machine for node'
    machine = machines[pos]
    result = []
    for dir in Dir:
      npos = getAdjacentPosition(pos, dir)
      if npos not in machines:
        machineCopy = machine.copy()
        output = machineCopy.addInput(dir).runUntilSingleOutput()
        values = ['#', '.', 'E']
        grid.setValue(npos, values[output])
        machines[npos] = machineCopy

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
  machine = IntcodeVM.initFromInput(input)

  grid = SparseGrid(2)
  result = explore(grid, machine)
  grid.print2D(default='*')
  print(result[1])

def part2() -> None:
  machine = IntcodeVM.initFromInput(input)

  grid = SparseGrid(2)
  result = explore(grid, machine)
  grid.print2D(default='*')
  start = result[0]
  print('end:', start)

  print(fillWithOxygen(grid, start))

part2()
