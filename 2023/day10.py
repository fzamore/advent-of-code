from collections import namedtuple
from enum import Enum
from common.arraygrid import ArrayGrid
from common.shortestpath import dijkstraAllNodes

input = open('day10.txt').read().splitlines()

Coords = namedtuple('Coords', ('x', 'y'))

# A "between point" represents the space between four points in a square.
# We represent it using a single coordinate pair for the northwest
# diagonal from the between point.
#
# So, the between point of (2, 1) represents the point between:
#   (2, 1), (3, 1), (3, 2), and (2, 2)
# OR
#   bp(x, y) is between: (x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)
#   draw a line northwest from bp to p

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

def canMoveInDirection(
  betweenPoint: Coords,
  delta: tuple[int, int],
  loopPoints: dict[Coords, str],
) -> bool:
  x, y = betweenPoint.x, betweenPoint.y
  # nw: (x, y), ne: (x + 1, y), se: (x + 1, y + 1), sw: (x, y + 1)
  match delta:
    case (-1, 0):
      p1, p2 = Coords(x, y), Coords(x, y + 1)
      v1, v2 = loopPoints.get(p1), loopPoints.get(p2)
      if v1 in ['|', 'F', '7']:
        return False
    case (1, 0):
      p1, p2 = Coords(x + 1, y), Coords(x + 1, y + 1)
      v1, v2 = loopPoints.get(p1), loopPoints.get(p2)
      if v1 in ['|', 'F', '7']:
        return False
    case (0, -1):
      p1, p2 = Coords(x, y), Coords(x + 1, y)
      v1, v2 = loopPoints.get(p1), loopPoints.get(p2)
      if v1 in ['-', 'F', 'L']:
        return False
    case (0, 1):
      p1, p2 = Coords(x + 1, y + 1), Coords(x, y + 1)
      v1, v2 = loopPoints.get(p1), loopPoints.get(p2)
      if v1 in ['-', 'J', '7']:
        return False
    case _:
      assert False, 'bad delta: %s' % str(delta)

  return True

# returns true if can escape grid
def dfs(
  betweenPoint: Coords,
  seenBetweenPoints: set[Coords],
  loopPoints: dict[Coords, str],
  width: int,
  height: int,
) -> bool:
  assert betweenPoint not in seenBetweenPoints, \
    'bad dfs: %s' % str(betweenPoint)
  seenBetweenPoints.add(betweenPoint)

  x, y = betweenPoint.x, betweenPoint.y
  if x < 0 or y < 0 or x >= width - 1 or y >= height - 1:
    # We have escaped the grid.
    return True

  deltas = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
  ]

  for d in deltas:
    if not canMoveInDirection(betweenPoint, d, loopPoints):
      continue
    dx, dy = d
    nextBetweenPoint = Coords(x + dx, y + dy)
    if nextBetweenPoint in seenBetweenPoints:
      continue

    result = dfs(
      nextBetweenPoint,
      seenBetweenPoints,
      loopPoints,
      width,
      height,
    )
    if result:
      return True

  # We haven't found a way out.
  return False

def traverseFromPoint(
  point: Coords,
  loopPoints: dict[Coords, str],
  innerPoints: set[Coords],
  outerPoints: set[Coords],
  width: int,
  height: int,
) -> None:
  if point in loopPoints or point in innerPoints or point in outerPoints:
    # We've already seen this point or it is on the loop. We don't care
    # about it.
    return

  seenBetweenPoints: set[Coords] = set()
  result = dfs(
    point,
    seenBetweenPoints,
    loopPoints,
    width,
    height,
  )

  for bp in seenBetweenPoints:
    x, y = bp.x, bp.y
    tuples = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
    for t in tuples:
      p = Coords(t[0], t[1])
      if p.x < 0 or p.x >= width or p.y < 0 or p.y >= height:
        continue
      if p in loopPoints:
        continue
      if result:
        assert p not in innerPoints, 'outer already in inner: %s' % str(p)
        outerPoints.add(p)
      else:
        assert p not in outerPoints, 'inner already in outer: %s' % str(p)
        innerPoints.add(p)


def printGrid(grid: ArrayGrid) -> None:
  # Wow, this is so much better. Thanks Aston.
  grid.print2D({
    '|': '║',
    '-': '═',
    'L': '╚',
    'J': '╝',
    '7': '╗',
    'F': '╔',
  })

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

def part2():
  grid, start = initGrid()
  width, height = grid.getWidth(), grid.getHeight()

  print('grid: %d x %d' % (width, height))
  print('start:', start)

  result = dijkstraAllNodes(
    start,
    lambda p: getAdjacentNodes(grid, p),
  )

  print('loop count:', len(result))
  loopPoints = {}
  for p in result:
    loopPoints[p] = grid.getValue(p.x, p.y)

  # Replace the start node with the correct pipe to make things easier
  # down the line.
  replacements = {
    '-': [(-1, 0), (1, 0)],
    'F': [(1, 0), (0, 1)],
    '7': [(-1, 0), (0, 1)],
    '|': [(0, -1), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    'L': [(1, 0), (0, -1)],
  }
  connections = {
    (-1, 0): ['F', 'L', '-'],
    (1, 0): ['J', '7', '-'],
    (0, -1): ['7', 'F' '|'],
    (0, 1): ['J', 'L', '|'],
  }
  for r in replacements:
    match = True
    for dx, dy in replacements[r]:
      p = Coords(start.x + dx, start.y + dy)
      if loopPoints.get(p) not in connections[(dx, dy)]:
        match = False
    if match:
      print('start match:', r)
      loopPoints[start] = r
      grid.setValue(start.x, start.y, r)

  # Remove non-loop pipe from the grid to ease debugging
  for y in range(height):
    for x in range(width):
      if grid.hasValue(x, y) and Coords(x, y) not in loopPoints:
        grid.setValue(x, y, '.')
  printGrid(grid)

  innerPoints = set()
  outerPoints = set()
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      traverseFromPoint(
        Coords(x, y),
        loopPoints,
        innerPoints,
        outerPoints,
        width,
        height,
      )

  print(len(outerPoints))
  print(len(innerPoints))

  assert \
    len(innerPoints) + len(outerPoints) + len(loopPoints) == width * height, \
    'all points not accounted for'

part2()
