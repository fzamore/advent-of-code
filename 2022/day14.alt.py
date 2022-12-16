from common.sparsegrid import Coords, SparseGrid
from itertools import pairwise

input = open('day14.txt').read().splitlines()

START: Coords = (500, 0)

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

# Recursively drops a grain of sand by first dropping all "children" of
# this grain (i.e., down, down-left, down-right). A grain of sand will
# come to rest if all of its children come to rest. Returns whether the
# sand was blocked (if False, the sand fell infinitely).
def dropSandDFS(
  grid: SparseGrid,
  coords: Coords,
  maxY: int,
  hasFloor: bool,
) -> bool:
  x, y = coords
  if y > maxY:
    # The sand has fallen past the lowest rock.
    if not hasFloor:
      # If there is no floor, it will fall infinitely.
      return False
    else:
      # Otherwise, it comes to rest on the "virtual" floor.
      grid.setValue(coords, 'o')
      return True

  for dx in [0, -1, 1]:
    ncoords = (x + dx, y + 1)
    if not grid.hasValue(ncoords):
      # If this child location is vacant, drop sand into it.
      if not dropSandDFS(grid, ncoords, maxY, hasFloor):
        # The child did not come to rest, and thus this grain won't
        # either.
        return False

  # This grain came to rest because all child locations are now blocked.
  grid.setValue(coords, 'o')
  return True

def part1():
  print('line count:', len(input))

  grid = SparseGrid(2)
  for line in input:
    addLineToGrid(grid, line)

  rockCount = len(grid.getAllCoords())
  maxY = grid.getMaxCoords()[1]

  print('points in grid:', rockCount)
  print('maxY', maxY)

  dropSandDFS(grid, START, maxY, hasFloor=False)
  grid.print2D(default='.')
  print(len(grid.getAllCoords()) - rockCount)

def part2():
  print('line count:', len(input))

  grid = SparseGrid(2)
  for line in input:
    addLineToGrid(grid, line)

  rockCount = len(grid.getAllCoords())
  maxY = grid.getMaxCoords()[1]

  print('points in grid:', rockCount)
  print('maxY', maxY)

  dropSandDFS(grid, START, maxY, hasFloor=True)
  print(len(grid.getAllCoords()) - rockCount)

part2()
