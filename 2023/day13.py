from common.arraygrid import ArrayGrid

input = open('day13.txt').read().split("\n\n")

def initGrids() -> list[ArrayGrid]:
  grids = []
  for gridStr in input:
    gridLines = gridStr.splitlines()
    w = len(gridLines[0])
    h = len(gridLines)
    grid = ArrayGrid(w, h)
    for y in range(h):
      for x in range(w):
        grid.setValue(x, y, gridLines[y][x])
    grids.append(grid)
    grid.print2D()
  return grids

def areRowsEqual(grid: ArrayGrid, y1: int, y2: int) -> bool:
  assert y1 < y2, 'bad equal row input'
  assert 0 <= y1 < grid.getHeight() - 1, 'bad y1: %d' % y1
  assert 0 <= y2 < grid.getHeight(), 'bad y2: %d' % y2

  for x in range(grid.getWidth()):
    if grid.getValue(x, y1) != grid.getValue(x, y2):
      return False
  return True

def isHorizReflection(grid: ArrayGrid, y: int) -> bool:
  h = grid.getHeight()
  assert 0 <= y < h - 1, 'bad horiz reflection input: %d' % y
  numRowsToCheck = min(y + 1, h - y - 1)
  for i in range(numRowsToCheck):
    if not areRowsEqual(grid, y - i, y + i + 1):
      return False
  return True

def areColsEqual(grid: ArrayGrid, x1: int, x2: int) -> bool:
  assert x1 < x2, 'bad equal row input'
  assert 0 <= x1 < grid.getWidth() - 1, 'bad x1: %d' % x1
  assert 0 <= x2 < grid.getWidth(), 'bad x2: %d' % x2

  for y in range(grid.getHeight()):
    if grid.getValue(x1, y) != grid.getValue(x2, y):
      return False
  return True

def isVertReflection(grid: ArrayGrid, x: int) -> bool:
  w = grid.getWidth()
  assert 0 <= x < w - 1, 'bad vert reflection input: %d' % x
  numColsToCheck = min(x + 1, w - x - 1)
  for i in range(numColsToCheck):
    if not areColsEqual(grid, x - i, x + i + 1):
      return False
  return True

def part1():
  grids = initGrids()

  print('grid count:', len(grids))

  r = 0
  for grid in grids:
    horizReflection = -1
    for y in range(grid.getHeight() - 1):
      if isHorizReflection(grid, y):
        assert horizReflection == -1, \
          'more than one horiz reflection found: %d, %d' % (y, horizReflection)
        horizReflection = y

    vertReflection = -1
    for x in range(grid.getWidth() - 1):
      if isVertReflection(grid, x):
        assert vertReflection == -1, \
          'more than one vert reflection found: %d, %d' % (x, vertReflection)
        vertReflection = x

    print(horizReflection, vertReflection)
    assert \
      (horizReflection != -1 or vertReflection != -1) and \
      (horizReflection == -1 or vertReflection == -1), \
      'exactly one horiz or vert should have been found: %d, %d' \
        % (horizReflection, vertReflection)

    r += 100 * (horizReflection + 1) + vertReflection + 1
  print(r)

part1()
