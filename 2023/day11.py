from itertools import combinations
from common.sparsegrid import SparseGrid

input = open('day11.txt').read().splitlines()

def initGrid(multiplier: int = 2) -> SparseGrid:
  width, height = len(input[0]), len(input)
  print('input: %d x %d' % (width, height))

  emptyCols = []
  for x in range(width):
    s = set([input[i][x] for i in range(height)])
    if len(s) == 1:
      emptyCols.append(x)

  emptyRows = []
  for y in range(height):
    s = set(input[y])
    if len(s) == 1:
      emptyRows.append(y)

  print('emptyCols:', emptyCols)
  print('emptyRows:', emptyRows)

  grid = SparseGrid(2)

  extraRowIndex = 0
  for y in range(height):
    if extraRowIndex < len(emptyRows) and y == emptyRows[extraRowIndex]:
      extraRowIndex += 1
    extraColIndex = 0
    for x in range(width):
      if extraColIndex < len(emptyCols) and x == emptyCols[extraColIndex]:
        extraColIndex += 1
      nx = x + extraColIndex * (multiplier - 1)
      ny = y + extraRowIndex * (multiplier - 1)
      v = input[y][x]
      if v == '#':
        grid.setValue((nx, ny), input[y][x])

  return grid

def part1():
  grid = initGrid()
  grid.print2D(default='.')

  result = 0
  for c1, c2 in combinations(grid.getAllCoords(), 2):
    x1, y1 = c1
    x2, y2 = c2
    manhattanDist = abs(x2 - x1) + abs(y2 - y1)
    result += manhattanDist
  print(result)

def part2():
  grid = initGrid(1000000)
  result = 0
  for c1, c2 in combinations(grid.getAllCoords(), 2):
    x1, y1 = c1
    x2, y2 = c2
    result += abs(x2 - x1) + abs(y2 - y1)
  print(result)

part1()
