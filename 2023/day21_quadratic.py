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

def part2() -> None:
  grid, start = initGrid()
  w, h = grid.getWidth(), grid.getHeight()
  print('grid size: (%d x %d)' % (w, h))
  print('start:', start)

  # This approach is heavily dependent on the input format and the target
  # value.

  # Each step will expand a diamond pattern by one unit in each cardinal
  # direction. It takes 65 steps to achive a perfect diamond (exactly one
  # reached space along each edge of the original w x h grid). This is
  # also the start x & y coordinate. Through experimentation, I discovered
  # that taking additional multiples of 131 steps (the grid width &
  # height), the diamond points will reach the edge in each additional
  # grid. It turns out that the target 26501365 number fits exactly into
  # the pattern 131k + 65, so the points of the target diamond will also
  # exactly reach the edges of some grid way off in the distance.
  #
  # In the cheatiest of the cheaty approaches, I learned from reddit that
  # incrementing k from [0, 1, 2, etc.] in the expression 131k + 65 will
  # increase the diamond size quadratically (no idea how this was
  # determined). This means that you can define f(x) = ax^2 + bx + c such
  # that x in this case is k (or the number of multiples of 131). So we
  # need to find a, b, and c, and then we have an algebraic function that
  # describes the answer.
  #
  # So, I manually computed the first three values of f(x) (which
  # correspond to 65, 196, 372 (k = [0, 1, 2]), which then gives us values
  # for f(0), f(1), and f(2). Via algebra, f(0) = c, and you can
  # subsititue to find a and b.

  # Ensure the start is in the center of the grid.
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

  f = {}
  cur = set([start])
  for i in range(n):
    cur = iterate(grid, cur)
    v = i + 1
    if v % w == extraSteps:
      f[floor(v / w)] = len(cur)
      print('f(%d): %d' % (v, len(cur)))

  print('fvalues:', f)

  # f(x) = ax^2 + bx + c
  c = f[0]
  assert (f[2] - 2) % 2 == 0, 'bad math'
  a = floor((f[2] - c) / 2) - (f[1] - c)
  b = f[1] - c - a

  ans = a * k * k + b * k + c
  print(ans)

part2()
