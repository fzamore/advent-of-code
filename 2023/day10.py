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
  incomingMoves = {
    (1, 0): set(['-', 'J', '7']),
    (-1, 0): set(['-', 'F', 'L']),
    (0, 1): set(['|', 'L', 'J']),
    (0, -1): set(['|', 'F', '7']),
  }
  outgoingMoves = {
    # The start node is eligible to go anywhere.
    'S': set(incomingMoves.keys()),
    '-': [(1, 0), (-1, 0)],
    '|': [(0, 1), (0, -1)],
    'L': [(0, -1), (1, 0)],
    'F': [(0, 1), (1, 0)],
    'J': [(0, -1), (-1, 0)],
    '7': [(0, 1), (-1, 0)],
  }
  v = grid.getValue(p.x, p.y, '.')
  if v not in outgoingMoves:
    return []
  for delta in outgoingMoves[v]:
    dx, dy = delta
    np = Coords(p.x + dx, p.y + dy)
    if grid.getValue(np.x, np.y, '.') in incomingMoves[delta]:
      results.append((np, 1))
  return results

def part1():
  grid, start = initGrid()

  print('grid: %d x %d' % (grid.getWidth(), grid.getHeight()))
  print('start:', start)

  # I think this makes the assumption that all reachable nodes from the
  # start are part of the loop.
  result = dijkstraAllNodes(
    start,
    lambda p: getAdjacentNodes(grid, p),
  )
  print(max(result.values()))

part1()
