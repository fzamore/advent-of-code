from typing import Optional
from common.arraygrid import ArrayGrid

input = open('day3.txt').read().splitlines()

def initGrid() -> ArrayGrid:
  grid = ArrayGrid(len(input[0]), len(input))
  for y in range(len(input)):
    for x in range(len(input[0])):
      assert len(input[y]) == grid.getWidth(), 'bad grid input'
      if input[y][x] != '.':
        grid.setValue(x, y, input[y][x])
  return grid

def isAdjacentToSymbol(grid: ArrayGrid, x: int, y: int) -> bool:
  assert grid.areCoordsWithinBounds(x, y), 'bad coords: %d, %d' % (x, y)
  assert grid.getValue(x, y).isdigit(), \
    'value at grid is not digit: %d, %d' % (x, y)

  for i in range(-1, 2):
    for j in range(-1, 2):
      if i == 0 and j == 0:
        continue
      nx = x + j
      ny = y + i
      if not grid.areCoordsWithinBounds(nx, ny):
        continue
      if grid.hasValue(nx, ny) and not grid.getValue(nx, ny).isdigit():
        return True
  return False

def getDigit(grid: ArrayGrid, x: int, y: int) -> Optional[int]:
  if not grid.hasValue(x, y):
    return None
  v = grid.getValue(x, y)
  if not v.isdigit():
    return None
  return int(v)

def part1():
  grid = initGrid()
  print(grid.getWidth(), grid.getHeight())

  grid.print2D({ None: '.' })

  sum = 0
  for y in range(grid.getHeight()):
    x = 0
    while x < grid.getWidth():
      n = 0
      v = getDigit(grid, x, y)
      isAdjacent = False
      while v is not None:
        if isAdjacentToSymbol(grid, x, y):
          isAdjacent = True
        n = 10 * n + v
        x += 1
        v = getDigit(grid, x, y)
      if isAdjacent and n != 0:
        sum += n
      x += 1
  print(sum)

part1()
