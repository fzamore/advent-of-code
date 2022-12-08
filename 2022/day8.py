from enum import Enum
from common.arraygrid import ArrayGrid
from math import prod

input = open('day8.txt').read().splitlines()

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

# O(m) or O(n). Iterates through exactly one row or column.
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

# O(mn). Computes visible cells in each row or col from a single
# direction. E.g., for NORTH, it computes the visible cells in each column
# starting from row 0. It will traverse the entire grid once.
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
    x, y = grid.getMaxX() - 1, grid.getMaxY() - 1

  visible = []
  while grid.areCoordsWithinBounds(x, y):
    visible.extend(getVisibleCellsInOneLine(grid, x, y, dx, dy))
    # these are intentionally switched so we advance to the next row or col
    x += dy
    y += dx
  return visible

# O(m) or O(n). Iterates through at most one entire row or column.
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
  print('dimensions: %d x %d' % (grid.getMaxX(), grid.getMaxY()))

  visible = set()
  for dir in Direction:
    visible |= set(getVisibleCellsFromOneDirection(grid, dir))
  print(len(visible))

# O(mn*(m+n)) -> O(n^3) (asuming a square). For each cell, traverse to the
# grid edge in all four directions.
def part2():
  grid = createGrid()
  print('dimensions: %d x %d' % (grid.getMaxX(), grid.getMaxY()))

  best = -1
  for x in range(0, grid.getMaxX()):
    for y in range(0, grid.getMaxY()):
      dist = prod(
        [getViewingDistanceInOneDirection(grid, x, y, d) for d in Direction],
      )
      if dist > best:
        best = dist
  print(best)

part2()
