from math import floor
from common.arraygrid import ArrayGrid

input = open('day21.txt').read().splitlines()

def initGrid() -> tuple[ArrayGrid, tuple[int, int]]:
  start = None
  grid = ArrayGrid(len(input[0]), len(input))
  for y in range(len(input)):
    for x in range(len(input[0])):
      grid.setValue(x, y, input[y][x])
      if input[y][x] == 'S':
        start = (x, y)
  assert start is not None
  # clear the start point in the grid for easier checking
  grid.setValue(start[0], start[1], '.')
  return grid, start

def canMove(grid: ArrayGrid, pos: tuple[int, int]) -> bool:
  x, y = pos
  # handle beyond the grid
  x %= grid.getWidth()
  y %= grid.getHeight()
  return grid.getValue(x, y, '#') != '#'

def iterate(grid: ArrayGrid, points: set[tuple[int, int]]) -> set[tuple[int, int]]:
  result = set()
  deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  for x, y in points:
    for dx, dy in deltas:
      nx, ny = x + dx, y + dy
      if canMove(grid, (nx, ny)):
        result.add((nx, ny))
  return result

def updateGrid(grid: ArrayGrid, cur: set[tuple[int, int]]) -> None:
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      if (x, y) in cur:
        grid.setValue(x, y, 1)
      elif grid.getValue(x, y) == 1:
        grid.setValue(x, y, 0)

def countCellsInShape(
  occupiedCells: set[tuple[int, int]],
  xrange: range,
  yrange: range,
) -> int:
  count = 0
  for x, y in occupiedCells:
    if x in xrange and y in yrange:
      count += 1
  return count

def countCellsInShapeRanges(
  occupiedCells: set[tuple[int, int]],
  ranges: list[tuple[range, range]],
) -> int:
  count = 0
  for xrange, yrange in ranges:
    count += countCellsInShape(occupiedCells, xrange, yrange)
  return count

def part1() -> None:
  grid, start = initGrid()
  grid.print2D()

  cur = set([start])
  for _ in range(64):
    cur = iterate(grid, cur)
  for x, y in cur:
    grid.setValue(x, y, 'O')
  grid.print2D()
  print(len(cur))

def part2() -> None:
  grid, start = initGrid()
  w, h = grid.getWidth(), grid.getHeight()
  print('grid size: (%d x %d)' % (w, h))
  print('start:', start)

  # This approach is heavily dependent on the input format and the target
  # value. It will not work on any of the sample inputs.

  # Each step will expand a diamond pattern by one unit in each cardinal
  # direction. It takes 65 steps to achive a perfect diamond (exactly one
  # space reached along each edge of the original w x h grid). This number
  # of steps (65) is also the start x & y coordinate. Through
  # experimentation, Each additional 131 steps (the grid width & height)
  # expands the diamond so that the diamond points reach the edge in an
  # additional grid. It turns out that the target 26501365 number fits
  # exactly into the pattern 131k + 65, so the points of the target
  # diamond will also exactly reach the edges of some grid way off in the
  # distance.
  #
  # My approach breaks the diamond into w x h-sized grid with a unique
  # occupied cell shape, counts the cells in each shape, and computes how
  # many occurrences of each shape will exist in the full diamond. To do
  # this, I iterate the original grid to k == 2 (131 * 2 + 65 == 327
  # steps), which is the minimum diamond size to achive each unique shape.

  # Ensure the start is at the center of the grid.
  assert (w - 1) / 2 == start[0], 'bad start x'
  assert (h - 1) / 2 == start[1], 'bad start y'
  assert w - 1 == start[0] * 2, 'bad grid size'

  # extraSteps is 65 here (the remainder in the 131k + 65 pattern).
  extraSteps = start[0]

  # Iterate until k == 2.
  n = 2 * w + extraSteps
  print('iterations:', n)

  target = 26501365
  k = floor(target / w)
  print('target:', target)
  print('k:', k)
  print('extra steps:', extraSteps)

  assert target % k == extraSteps, 'bad math'

  print('iterating...')
  occupiedCells = set([start])
  for _ in range(n):
    occupiedCells = iterate(grid, occupiedCells)
    updateGrid(grid, occupiedCells)

  print('all cells:', len(occupiedCells))
  print()

  # "point" shape. There will always be exactly four of these (one at each
  # point of the diamond).
  pointRanges = [
    (range(0, w), range(-2 * h, -h)),
    (range(0, w), range(2 * h, 3 * h)),
    (range(-2 * w, -w), range(0, h)),
    (range(2 * w, 3 * w), range(0, h)),
  ]
  pointCellsCount = countCellsInShapeRanges(occupiedCells, pointRanges)
  print('pointCells:', pointCellsCount)

  # "large" diagonal shape. The diamond edges do not cut across square
  # grids evenly, so there will be large diagonals and small diagonals.
  largeDiagonalRanges = [
    (range(-w, 0), range(-h, 0)), # nw
    (range(w, 2 * w), range(-h, 0)), # ne
    (range(-w, 0), range(h, 2 * h)), # sw
    (range(w, 2 * w), range(h, 2 * h)), # se
  ]
  largeDiagonalCellsCount = countCellsInShapeRanges(occupiedCells, largeDiagonalRanges)
  print('largeDiagonalCells:', largeDiagonalCellsCount)

  # "small" diagonal shape. There will always be more of these than the
  # large diagonal shape.
  smallDiagonalRanges = [
    (range(-2 * w, -w), range(-h, 0)), # nw (lower)
    (range(-w, 0), range(-2 * h, -h)), # nw (higher)
    (range(2 * w, 3 * w), range(-h, 0)), # ne (lower)
    (range(w, 2 * w), range(-2 * h, -h)), # ne (higher)
    (range(-2 * w, -w), range(h, 2 * h)), # sw (higher)
    (range(-w, 0), range(2 * h, 3 * h)), # sw (lower)
    (range(2 * w, 3 * w), range(h, 2 * h)), # se (higher)
    (range(w, 2 * w), range(2 * h, 3 * h)), # se (lower)
  ]
  smallDiagonalCellsCount = countCellsInShapeRanges(occupiedCells, smallDiagonalRanges)
  print('smallDiagonalCells:', smallDiagonalCellsCount)

  # "start" shape. This is the square w x h grid that contains the start
  # point. The squares completely within the diamond will alternate
  # between "start" and "non-start" shapes.
  startRange = (range(w), range(h))
  startCellsCount = countCellsInShapeRanges(occupiedCells, [startRange])
  print('startCells:', startCellsCount)

  # "non-start" shape.
  nonStartRange = (range(w, 2 * w), range(h))
  nonStartCellsCount = countCellsInShapeRanges(occupiedCells, [nonStartRange])
  print('nonStartCells:', nonStartCellsCount)

  pointShapeCount = 1 # groups of four
  largeDiagonalShapeCount = k - 1 # groups of four
  smallDiagonalShapeCount = k # groups of four
  startShapeCount = (k - 1) * (k - 1)
  nonStartShapeCount = k * k

  print('pointCount:', pointShapeCount)
  print('largeDiagonalCount:', largeDiagonalShapeCount)
  print('smallDiagonalCount:', smallDiagonalShapeCount)
  print('startCount:', startShapeCount)
  print('nonStartCount:', nonStartShapeCount)

  # Small diagonal cells are counted in groups of 8, so we need to divide
  # by two.
  assert smallDiagonalCellsCount % 2 == 0, 'bad small diagonal cells'
  smallDiagonalCellsCount //= 2

  ans = \
    pointShapeCount * pointCellsCount + \
    largeDiagonalShapeCount * largeDiagonalCellsCount + \
    smallDiagonalShapeCount * smallDiagonalCellsCount + \
    startShapeCount * startCellsCount + \
    nonStartShapeCount * nonStartCellsCount

  print(ans)

part2()
