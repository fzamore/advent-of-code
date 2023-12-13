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

def findHorizReflection(grid: ArrayGrid, origReflection: int = -1) -> int:
  reflection = -1
  for y in range(grid.getHeight() - 1):
    if y == origReflection:
      continue
    if isHorizReflection(grid, y):
      assert reflection == -1, \
        'more than one horiz reflection found: %d, %d' % (y, reflection)
      reflection = y
  return reflection

def findVertReflection(grid: ArrayGrid, origReflection: int = -1) -> int:
  reflection = -1
  for x in range(grid.getWidth() - 1):
    if x == origReflection:
      continue
    if isVertReflection(grid, x):
      assert reflection == -1, \
        'more than one vert reflection found: %d, %d' % (x, reflection)
      reflection = x
  return reflection

def smudgeAndfindReflections(
    grid: ArrayGrid,
    origHorizReflection: int,
    origVertReflection: int,
  ) -> tuple[int, int]:
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      # smudge!
      v = grid.getValue(x, y)
      nv = '#' if v == '.' else '.'
      grid.setValue(x, y, nv)

      horizReflection = findHorizReflection(grid, origHorizReflection)
      if horizReflection != -1:
        print('new horiz:', horizReflection)
        # unsmudge
        grid.setValue(x, y, v)
        return (horizReflection, -1)

      vertReflection = findVertReflection(grid, origVertReflection)
      if vertReflection != -1:
        print('new vert:', vertReflection)
        vertReflection = vertReflection
        # unsmudge
        grid.setValue(x, y, v)
        return (-1, vertReflection)
      # unsmudge
      grid.setValue(x, y, v)

  assert False, 'did not find new horiz or vert reflection'

def part1():
  grids = initGrids()

  print('grid count:', len(grids))

  r = 0
  for grid in grids:
    horizReflection = findHorizReflection(grid)
    vertReflection = findVertReflection(grid)
    print(horizReflection, vertReflection)

    assert \
      (horizReflection != -1 or vertReflection != -1) and \
      (horizReflection == -1 or vertReflection == -1), \
      'exactly one horiz or vert should have been found: %d, %d' \
        % (horizReflection, vertReflection)

    r += 100 * (horizReflection + 1) + vertReflection + 1
  print(r)

def part2():
  grids = initGrids()

  print('grid count:', len(grids))

  r = 0
  for grid in grids:
    print()
    horizReflection = -1
    vertReflection = -1
    origHorizReflection = findHorizReflection(grid)
    origVertReflection = findVertReflection(grid)
    print('initial:', origHorizReflection, origVertReflection)
    assert \
      (origHorizReflection != -1 or origVertReflection != -1) and \
      (origHorizReflection == -1 or origVertReflection == -1), \
      'exactly one horiz or vert should have been found: %d, %d' \
        % (origHorizReflection, origVertReflection)

    horizReflection, vertReflection = smudgeAndfindReflections(
      grid,
      origHorizReflection,
      origVertReflection,
    )

    assert \
      (horizReflection != -1 or vertReflection != -1) and \
      (horizReflection == -1 or vertReflection == -1), \
      'exactly one horiz or vert should have been found: %d, %d' \
        % (horizReflection, vertReflection)

    r += 100 * (horizReflection + 1) + vertReflection + 1
  print(r)

part2()
