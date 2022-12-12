from typing import Iterator
from common.arraygrid import ArrayGrid
from common.shortestpath import dijkstra

Coords = tuple[int, int]

input = open('day12.txt').read().splitlines()

def parseInput(input: list[str]) -> tuple[ArrayGrid, Coords]:
  start = (-1, -1)
  grid = ArrayGrid(len(input[0]), len(input))
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      value = input[y][x]
      if value == 'S':
        start = (x, y)
      grid.setValue(x, y, input[y][x])
  return (grid, start)

def getNumericValue(value: str) -> int:
  match value:
    case 'S': return ord('a')
    case 'E': return ord('z')
    case v: return ord(v)

def canMoveIntoCell(grid: ArrayGrid, value: str, x: int, y: int) -> bool:
  if not grid.areCoordsWithinBounds(x, y):
    return False
  nv = grid.getValue(x, y)
  return getNumericValue(nv) <= getNumericValue(value) + 1

def getAdjacentCells(
  grid: ArrayGrid,
  x: int,
  y: int,
) -> Iterator[tuple[Coords, int]]:
  deltas = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
  ]
  v = grid.getValue(x, y)
  for delta in deltas:
    nx, ny = x + delta[0], y + delta[1]
    if canMoveIntoCell(grid, v, nx, ny):
      # Return a score of 1 with each adjacent cell.
      yield ((nx, ny), 1)

def isDone(grid: ArrayGrid, x: int, y: int) -> bool:
  return grid.getValue(x, y) == 'E'

def part1():
  grid, start = parseInput(input)
  print('%d x %d' % (grid.getWidth(), grid.getHeight()))
  print('start:', start)

  result = dijkstra(
    start,
    lambda node: getAdjacentCells(grid, node[0], node[1]),
    lambda node: isDone(grid, node[0], node[1]),
  )

  print(result)
  print(result[1])

def part2():
  grid, _ = parseInput(input)
  print('%d x %d' % (grid.getWidth(), grid.getHeight()))

  starts = []
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      if grid.getValue(x, y) == 'a' or grid.getValue(x, y) == 'S':
        starts.append((x, y))

  print('number of start positions:', len(starts))

  # add a new start position such that it has edges of weight zero to each
  # of the "real" start positions
  start = (-1, -1)
  def getAdjecentCells2(node: Coords) -> Iterator[tuple[Coords, int]]:
    if node == start:
      for s in starts:
        yield (s, 0)
      return

    yield from getAdjacentCells(grid, node[0], node[1])

  def isDone2(node: Coords) -> bool:
    return node != start and isDone(grid, node[0], node[1])

  result = dijkstra(
    start,
    getAdjecentCells2,
    isDone2,
  )

  print(result)
  print(result[1])

part2()
