from collections import namedtuple
from enum import Enum
from common.arraygrid import ArrayGrid
from common.shortestpath import dijkstraAllNodes

input = open('day10.txt').read().splitlines()

Coords = namedtuple('Coords', ('x', 'y'))

# The algorithm assumes that the loop containing the start is well-formed,
# and that any pieces of pipe that aren't along this loop can be
# discarded and treated as if there was no pipe there.

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

# Returns whether the DFS is allowed to move in the given direction from
# the given between point.
def canMoveInDirection(
  betweenPoint: Coords,
  delta: tuple[int, int],
  loopPoints: dict[Coords, str],
) -> bool:
  x, y = betweenPoint.x, betweenPoint.y

  # Translation between delta and point to check.
  deltaMap = {
    (-1, 0): (0, 0),
    (1, 0): (1, 0),
    (0, -1): (0, 0),
    (0, 1): (0, 1),
  }

  # Values that the point cannot be.
  disallowedValues = {
    (-1, 0): ('|', 'F', '7'),
    (1, 0): ('|', 'F', '7'),
    (0, -1): ('-', 'F', 'L'),
    (0, 1): ('-', 'F', 'L'),
  }

  dx, dy = deltaMap[delta]
  v = loopPoints.get(Coords(x + dx, y + dy))
  if v in disallowedValues[delta]:
    return False
  return True

# Performs a DFS starting at the given between point. Returns true if
# there is a path from this between point to the outside of the grid.
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

# Performs a "traversal" from this point by starting a DFS from the
# between point associated with this point. it updates the innerPoints and
# outerPoints sets based on which points are found to be enclosed vs. have
# a path to exit the grid.
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

  # The between points along this DFS traversal are either all enclosed,
  # or all exposed, depending on the result of the DFS. Update the sets as
  # needed.
  for bp in seenBetweenPoints:
    x, y = bp.x, bp.y
    tuples = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
    for t in tuples:
      p = Coords(t[0], t[1])
      if p.x < 0 or p.x >= width or p.y < 0 or p.y >= height:
        # This point is outside the grid.
        continue
      if p in loopPoints:
        # Points in the loop are neither inner or outer.
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

  # Run dijkstra to get distances from the start node to all other nodes.
  # This makes the assumption that all reachable nodes from the start are
  # part of the loop.
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

  # Dijkstra is certainly overkill here, since I only care about
  # identifying the loop, but I already had it from part 1.
  result = dijkstraAllNodes(
    start,
    lambda p: getAdjacentNodes(grid, p),
  )

  print('loop count:', len(result))
  loopPoints = {}
  for p in result:
    loopPoints[p] = grid.getValue(p.x, p.y)

  # Replace the start node with its underlying pipe to make things easier.
  adjStartNodes = getAdjacentNodes(grid, start)
  assert len(adjStartNodes) == 2, 'start node should have 2 adj nodes'
  replacements = {
    frozenset(((-1, 0), (1, 0))): '-',
    frozenset(((1, 0), (0, 1))): 'F',
    frozenset(((-1, 0), (0, 1))): '7',
    frozenset(((0, -1), (0, 1))): '|',
    frozenset(((-1, 0), (0, -1))): 'J',
    frozenset(((1, 0), (0, -1))): 'L',
  }
  key = []
  for (nx, ny), _ in adjStartNodes:
    dx, dy = nx - start.x, ny - start.y
    key.append((dx, dy))
  r = replacements[frozenset(key)]
  print('start match:', r)
  loopPoints[start] = r
  grid.setValue(start.x, start.y, r)

  # Remove non-loop pipe from the grid to ease debugging.
  for y in range(height):
    for x in range(width):
      if grid.hasValue(x, y) and Coords(x, y) not in loopPoints:
        grid.setValue(x, y, '.')
  printGrid(grid)

  innerPoints = set()
  outerPoints = set()
  # Start a traversal from every grid point.
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

  assert \
    len(innerPoints) + len(outerPoints) + len(loopPoints) == width * height, \
    'all points not accounted for'

  print(len(outerPoints))
  print(len(innerPoints))

part2()
