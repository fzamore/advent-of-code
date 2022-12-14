from common.sparsegrid import Coords, SparseGrid
from itertools import pairwise

input = open('day14.txt').read().splitlines()

START = (500, 0)
INF = (0, -1) # Impossible for the sand to float up, so use this as a marker.

def addLineToGrid(grid: SparseGrid, line: str) -> None:
  pairs = pairwise(line.split(' -> '))
  for p1, p2 in pairs:
    x1, y1 = map(int, p1.split(','))
    x2, y2 = map(int, p2.split(','))
    assert x1 == x2 or y1 == y2, 'bad input line: %s' % line
    assert x1 != x2 or y1 != y2, 'points are equal in line: %s' % line
    px, py = x1, y1
    while px != x2 or py != y2:
      grid.setValue((px, py), '#')
      if x1 == x2:
        py += 1 if y2 > y1 else -1
      else:
        px += 1 if x2 > x1 else -1
    # the loop stops too early
    grid.setValue((x2, y2), '#')

def hasFallenTooFar(grid: SparseGrid, coords: Coords) -> bool:
  # Past the bottom of the lowest rock.
  return coords[1] > grid.getMaxCoords()[1]

def getNextSandCoords(grid: SparseGrid, coords: Coords) -> Coords:
  if hasFallenTooFar(grid, coords):
    return INF

  x, y = coords
  deltas = [
    (0, 1), # down
    (-1, 1), # down-left
    (1, 1,), # down-right
  ]
  for dx, dy in deltas:
    nx, ny = x + dx, y + dy
    if not grid.hasValue((nx, ny)):
      # The space is free. Fall into it.
      return (nx, ny)

  # The sand was unable to move. Return its current position.
  return coords

def addSand(grid: SparseGrid, start: Coords = START) -> Coords:
  cur, next = start, start
  while (next := getNextSandCoords(grid, cur)) not in [INF, cur]:
    cur = next

  if next != INF:
    # Add the sand to the grid.
    grid.setValue(next, 'o')
  return next

def part1():
  print('line count:', len(input))

  grid = SparseGrid(2)
  for line in input:
    addLineToGrid(grid, line)

  print('points in grid:', len(grid.getAllCoords()))
  print('START GRID')
  grid.print2D(default='.')
  print('')

  i = 0
  while addSand(grid) != INF:
    i += 1

  print('FINISHED GRID')
  grid.print2D(default='.')
  print('')
  print(i)

part1()
