from enum import Enum
from common.arraygrid import ArrayGrid
from math import prod

input = open('day8.txt').read().splitlines()

# All running times assume the grid is a square, though I believe the code
# should work if it were a rectangle.

class Direction(Enum):
  NORTH = 1
  EAST = 2
  SOUTH = 3
  WEST = 4

# O(n^2)
def createGrid() -> ArrayGrid:
  grid = ArrayGrid(len(input[0]), len(input))
  y = 0
  for line in input:
    for x in range(0, len(line)):
      grid.setValue(x, y, int(line[x]))
    y += 1
  return grid

# O(n). Iterates through exactly one row or column.
def getVisibleCellsInOneLine(
  grid: ArrayGrid,
  sx: int,
  sy: int,
  dx: int,
  dy: int,
) -> list[tuple[int, int]]:
  visible, max = [], -1
  x, y = sx, sy
  while grid.areCoordsWithinBounds(x,y):
    if grid.getValue(x, y) > max:
      visible.append((x, y))
      max = grid.getValue(x, y)
    x += dx
    y += dy
  return visible

# O(n^2). Computes visible cells in each row or col from a single
# direction. E.g., for NORTH, it computes the visible cells in each column
# starting from the top (row 0). It will traverse the entire grid once.
def getVisibleCellsFromOneDirection(
  grid: ArrayGrid,
  direction: Direction,
) -> list[tuple[int, int]]:
  dx, dy = {
    Direction.NORTH: (0, 1),
    Direction.EAST: (-1, 0),
    Direction.SOUTH: (0, -1),
    Direction.WEST: (1, 0),
  }[direction]
  if direction in [Direction.NORTH, Direction.WEST]:
    x, y = 0, 0
  else:
    x, y = grid.getWidth() - 1, grid.getHeight() - 1

  visible = []
  while grid.areCoordsWithinBounds(x, y):
    visible.extend(getVisibleCellsInOneLine(grid, x, y, dx, dy))
    # these are intentionally switched so we advance to the next row or col
    x += dy
    y += dx
  return visible

# O(n). Iterates through at most one entire row or column.
def getViewingDistanceInOneDirection(
  grid: ArrayGrid,
  x: int,
  y: int,
  direction: Direction,
) -> int:
  dx, dy = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
  }[direction]
  v = grid.getValue(x, y)
  x, y = x + dx, y + dy
  c = 0
  while grid.areCoordsWithinBounds(x, y):
    c += 1
    if grid.getValue(x, y) >= v:
      break
    x += dx
    y += dy
  return c

# O(nm), since it calls getVisibleCellsFromOneDirection() four times.
def part1():
  grid = createGrid()
  print('dimensions: %d x %d' % (grid.getWidth(), grid.getHeight()))

  visible = set()
  for dir in Direction:
    # The call to getVisibleCellsFromOneDirection() is O(n^2). Doing a
    # union with the existing set is O(n), so this entire loop is
    # O(4 * (O(n^2) + O(n)) = O(n^2).
    visible |= set(getVisibleCellsFromOneDirection(grid, dir))
  print(len(visible))

# O(n^3). For each cell, traverse to the grid edge in all four directions.
def part2():
  grid = createGrid()
  print('dimensions: %d x %d' % (grid.getWidth(), grid.getHeight()))

  best = -1
  for x in range(0, grid.getWidth()):
    for y in range(0, grid.getHeight()):
      dist = prod(
        [getViewingDistanceInOneDirection(grid, x, y, d) for d in Direction],
      )
      if dist > best:
        best = dist
  print(best)

part2()
