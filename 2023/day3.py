from collections import namedtuple
import math
from typing import Optional
from common.arraygrid import ArrayGrid

input = open('day3.txt').read().splitlines()

# We need startX and startY so each Entry is unique when compared by value
Entry = namedtuple('Entry', ['value', 'startX', 'startY'])

# Grid stores either a character (if a non-numeric, non-period) or an
# Entry, at each cell
def initGrid() -> ArrayGrid:
  grid = ArrayGrid(len(input[0]), len(input))
  for y in range(len(input)):
    x = 0
    while x < len(input[0]):
      assert len(input[y]) == grid.getWidth(), 'bad grid input'
      v = input[y][x]
      if not v.isdigit():
        if v != '.':
          grid.setValue(x, y, v)
        x += 1
        continue
      n = 0
      nx = x
      while nx < len(input[0]) and input[y][nx].isdigit():
        n = 10 * n + int(input[y][nx])
        nx += 1
      e = Entry(n, x, y)
      for i in range(x, nx):
        grid.setValue(i, y, e)
      x = nx
  return grid

def isAdjacentToSymbol(grid: ArrayGrid, x: int, y: int) -> bool:
  assert grid.areCoordsWithinBounds(x, y), 'bad coords: %d, %d' % (x, y)
  for i in range(-1, 2):
    for j in range(-1, 2):
      if i == 0 and j == 0:
        continue
      nx = x + j
      ny = y + i
      if not grid.areCoordsWithinBounds(nx, ny):
        continue
      if not grid.hasValue(nx, ny):
        continue
      if not isinstance(grid.getValue(nx, ny), Entry):
        # if the adjacent value in the grid is not a numerical entry
        return True
  return False

def getGearRatio(grid: ArrayGrid, x: int, y: int) -> int:
  assert grid.getValue(x, y) == '*', 'bad coords to getGearRatio'
  # Use a set to keep track of adjacent entries so we get deduping.
  adjacentEntries = set()
  for i in range(-1, 2):
    for j in range(-1, 2):
      if i == 0 and j == 0:
        continue
      nx = x + j
      ny = y + i
      if not grid.areCoordsWithinBounds(nx, ny):
        continue
      v = grid.getValue(nx, ny)
      if isinstance(v, Entry):
        adjacentEntries.add(v)
  if len(adjacentEntries) == 2:
    return math.prod([e.value for e in adjacentEntries])
  else:
    return 0

def part1():
  grid = initGrid()
  print(grid.getWidth(), grid.getHeight())

  s = set()
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      v = grid.getValue(x, y)
      if isinstance(v, Entry) and isAdjacentToSymbol(grid, x, y):
        s.add(v)

  values = [x.value for x in s]
  print(len(values))
  print(sum(values))

def part2():
  grid = initGrid()
  print(grid.getWidth(), grid.getHeight())

  sum = 0
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      v = grid.getValue(x, y)
      if v == '*':
        ratio = getGearRatio(grid, x, y)
        sum += ratio
  print(sum)

part2()
