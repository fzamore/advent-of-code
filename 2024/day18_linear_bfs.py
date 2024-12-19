from typing import Iterable, Optional
from common.arraygrid import ArrayGrid
from common.ints import ints
from common.graphtraversal import bfs

input = open('day18.txt').read().splitlines()

Coords = tuple[int, int]

def parseInput(width: int, height: int, n: int) -> ArrayGrid:
  grid = ArrayGrid(width, height)
  for i in range(n):
    x, y = ints(input[i])
    grid.setValue(x, y, '#')
  return grid

def getAdjacent(grid: ArrayGrid, coords: Coords) -> Iterable[Coords]:
  x, y = coords
  for ax, ay in grid.getAdjacentCoords(x, y):
    v = grid.getValue(ax, ay)
    if v != '#':
      yield ax, ay

def search(grid: ArrayGrid, start: Coords, end: Coords) -> Optional[int]:
  r = bfs(
    start,
    lambda p: getAdjacent(grid, p),
    isEndNode=lambda p: p == end,
  )
  return r.get(end)

def part1() -> None:
  xMax, yMax = 70, 70
  n = 1024

  grid = parseInput(xMax + 1, yMax + 1, n)
  grid.print2D({None: '.'})

  start = 0, 0
  end = xMax, yMax

  print(search(grid, start, end))

def part2() -> None:
  xMax, yMax = 70, 70

  start = 0, 0
  end = xMax, yMax

  print('input:', len(input))

  # From Part 1 we know we can start at 1024. Still, this linear search is
  # slow (compared to a binary search).
  for i in range(1024, len(input)):
    grid = parseInput(xMax + 1, yMax + 1, i)
    result = search(grid, start, end)
    if result is None:
      print('done. i:', i)
      print(input[i - 1])
      return

  assert False, 'did not finish'

part2()
