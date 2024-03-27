from collections import namedtuple
import sys
from typing import Optional
from common.arraygrid import ArrayGrid

# This algorithm solves the puzzle "Snakes Inside Boxes" from the
# September 2023 isssue of GAMES Magazine. Each input is a square grid,
# where each cell is either empty or contains a number. At each number
# starts a snake whose length is indicated by the number. Snakes can go
# straight or turn at right angles, but no 2x2 area of boxes may contain
# the same snake.

Coords = tuple[int, int]
Snake = namedtuple('Snake', ['length', 'start'])
Region = set[Coords]

# Returns all four 2x2 boxes that contain the given point.
def getBoxes(pos: Coords) -> list[list[Coords]]:
  result = []
  x, y = pos
  for dx in [-1, 1]:
    nx = x + dx
    for dy in [-1, 1]:
      result.append([(nx, y + dy), (nx, y), (x, y + dy), (x, y)])
  assert len(result) == 4, 'should be four boxes'
  return result

# Returns whether the given point makes a 2x2 box with the given path (and
# thus is an illegal placement for a snake).
def makesBox(path: list[Coords], pos: Coords) -> bool:
  npath = path + [pos]
  for box in getBoxes(pos):
    if all([(bx, by) in npath for (bx, by) in box]):
      return True
  return False

# Adds the given path to the grid for pretty printing.
def addPathToGrid(grid: ArrayGrid, path: list[Coords]) -> None:
  markers = {
    ((0, 1), (0, 1)): '║',
    ((0, 1), (-1, 0)): '╝',
    ((0, 1), (1, 0)): '╚',

    ((0, -1), (0, -1)): '║',
    ((0, -1), (-1, 0)): '╗',
    ((0, -1), (1, 0)): '╔',

    ((1, 0), (1, 0)): '═',
    ((1, 0), (0, -1)): '╝',
    ((1, 0), (0, 1)): '╗',

    ((-1, 0), (-1, 0)): '═',
    ((-1, 0), (0, -1)): '╚',
    ((-1, 0), (0, 1)): '╔',
  }

  endcaps = {
    (-1, 0): '╞',
    (1, 0): '╡',
    (0, -1): '╥',
    (0, 1): '╨',
  }

  for i in range(len(path) - 1):
    x, y = path[i + 1]
    px, py = path[i]
    dx1, dy1 = x - px, y - py
    assert dx1 != 0 or dy1 != 0, 'bad deltas'

    if i < len(path) - 2:
      nx, ny = path[i + 2]
      dx2, dy2 = nx - x, ny - y
      assert dx2 != 0 or dy2 != 0, 'bad deltas'
      v = markers[(dx1, dy1), (dx2, dy2)]
    else:
      v = endcaps[dx1, dy1]

    grid.setValue(x, y, v)

# Computes a "region" of open cells in the grid, starting at the given
# point.
def computeRegion(grid: ArrayGrid, start: Coords) -> Region:
  assert grid.getValue(start[0], start[1]) == '.', 'grid occupied in region'

  q = [start]
  seen = set([start])

  # DFS.
  while len(q) > 0:
    x, y = q.pop()
    for nx, ny in grid.getAdjacentCoords(x, y):
      if grid.getValue(nx, ny) != '.':
        # Ignore occupied cells.
        continue

      if (nx, ny) in seen:
        continue
      seen.add((nx, ny))
      q.append((nx, ny))

  return seen

# Computes all regions of open cells within the grid.
def computeGridRegions(grid: ArrayGrid) -> list[Region]:
  allOpenCells = set()
  regions = []
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      if grid.getValue(x, y) != '.':
        continue

      if (x, y) in allOpenCells:
        continue

      region = computeRegion(grid, (x, y))
      assert (x, y) in region, 'region did not include start'

      allOpenCells.update(region)
      regions.append(region)

  return regions

# Returns whether the given region is "valid". Specifically, whether it's
# possible for a snake to be placed within it, meaning the region borders
# at least one snake starting point and the region is large enough to fit
# that snake. If the region is invalid, the entire grid is a dead-end and
# cannot yield a solution.
def isValidRegion(
  grid: ArrayGrid,
  snakes: list[Snake],
  si: int,
  path: list[Coords],
  region: Region,
) -> bool:
  n = len(region)
  for x, y in region:
    for nx, ny in grid.getAdjacentCoords(x, y):
      if (nx, ny) == path[-1] and n >= snakes[si].length - len(path) - 1:
        # We can reach the end of the current path and the region is large
        # enough to accommodate the remainder of the current snake.
        return True

      for i in range(si + 1, len(snakes)):
        if (nx, ny) == snakes[i].start and n >= snakes[i].length - 1:
          # There is an adjacent snake start-point and the region is large
          # enough to accommodate that snake.
          return True

  return False

# Recursively place snakes in the grid, starting with the "current" snake
# at the given index and the path for the current snake placed so far.
def placeSnakes(
  grid: ArrayGrid,
  snakes: list[Snake],
  si: int = 0,
  path: list[Coords] = [],
) -> Optional[ArrayGrid]:
  if si == len(snakes):
    # We're finished.
    return grid

  snake = snakes[si]
  if len(path) == 0:
    path = [snake.start]

  x, y = path[-1]
  assert grid.getValue(x, y) != '.', 'snake was not placed'

  for nx, ny in grid.getAdjacentCoords(x, y):
    if grid.getValue(nx, ny) != '.':
      # This cell is occupied. We can not place a snake here.
      continue

    if makesBox(path, (nx, ny)):
      # Placing a snake here would yield an illegal 2x2 box.
      continue

    # This optimization is crucial for pruning invalid solutions.
    regions = computeGridRegions(grid)
    if not all([isValidRegion(grid, snakes, si, path, r) for r in regions]):
      # Placing a snake here would yield at least one invalid region.
      continue

    # Place the section of snake here.
    ngrid = grid.copy()
    ngrid.setValue(nx, ny, '#')

    nsi = si
    npath = path + [(nx, ny)]
    if len(npath) == snake.length:
      # We're finished with this snake. Move on to the next one.
      addPathToGrid(ngrid, npath)
      nsi += 1
      npath = []

    result = placeSnakes(ngrid, snakes, nsi, npath)
    if result is not None:
      # We found a result. Return it.
      return result

  return None

def solve(filename: str) -> None:
  input = open(filename).read().splitlines()
  grid = ArrayGrid.gridFromInput(input)
  w, h = grid.getWidth(), grid.getHeight()
  assert w == h, 'grid should be square'
  grid.print2D()
  totalLength = 0

  snakes = []
  for y in range(w):
    for x in range(h):
      v = grid.getValue(x, y)
      if v == '.':
        continue

      if v.isdigit():
        length = int(v)
      elif v.isupper():
        # Use uppercase letters for two-digit numbers (e.g., J for 10, K
        # for 11, etc.).
        length = int(ord(v) - ord('A')) + 1
      else:
        assert False, 'bad grid value: %s' % v

      print('snake:', v, length)
      totalLength += length
      snakes.append(Snake(length, (x, y)))

  print()
  print('number of snakes:', len(snakes))
  assert totalLength == w * h, 'bad total snakes'

  result = placeSnakes(grid, snakes)
  if result is None:
    print('no result')
  else:
    result.print2D()

filename = sys.argv[1] if len(sys.argv) == 2 else 'snake0.txt'
solve(filename)
