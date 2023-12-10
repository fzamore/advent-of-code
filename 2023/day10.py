from collections import namedtuple
from common.arraygrid import ArrayGrid
from common.shortestpath import dijkstraAllNodes

input = open('day10.txt').read().splitlines()

Coords = namedtuple('Coords', ['x', 'y'])

def initGrid() -> tuple[ArrayGrid, Coords]:
  width, height = len(input[0]), len(input)

  start = None
  grid = ArrayGrid(width, height)
  for y in range(height):
    for x in range(width):
      v = input[y][x]
      grid.setValue(x, y, v)
      if v == 'S':
        start = Coords(x, y)

  assert start is not None, 'did not find start'
  return grid, start

def getAdjacentNodes(grid: ArrayGrid, p: Coords) -> list[tuple[Coords, int]]:
  results = []
  possibleMoves = {
    (1, 0): set(['-', '7', 'J']),
    (-1, 0): set(['-', 'L', 'F']),
    (0, -1): set(['|', 'F', '7']),
    (0, 1): set(['|', 'L', 'J']),
  }
  for delta in possibleMoves:
    dx, dy = delta
    values = possibleMoves[delta]
    np = Coords(p.x + dx, p.y + dy)
    if grid.getValue(np.x, np.y, '.') in values:
      results.append((np, 1))
  return results

def part1():
  grid, start = initGrid()

  print('grid: %d x %d' % (grid.getWidth(), grid.getHeight()))
  print('start:', start)

  result = dijkstraAllNodes(
    start,
    lambda p: getAdjacentNodes(grid, p),
  )
  print(max(result.values()))

part1()
