from common.arraygrid import ArrayGrid

serial = int(open('day11.txt').read())

MIN = 1
MAX = 300

def getPower(x: int, y: int, serial: int) -> int:
  rackID = x + 10
  power = (rackID * y + serial) * rackID
  return (power // 100) % 10 - 5

def getPowerSquare(x: int, y: int, serial: int, n: int = 3) -> int:
  s = 0
  for xi in range(x, x + n):
    for yi in range(y, y + n):
      assert MIN <= x <= MAX, 'bad x'
      assert MIN <= y <= MAX, 'bad y'
      s += getPower(xi, yi, serial)
  return s

def getPowerSquareFromGrid(grid: ArrayGrid, x: int, y: int, n: int) -> int:
  if x + n > MAX + 1 or y + n > MAX + 1:
    return -10000

  return \
    grid.getValue(x, y, 0) \
    - grid.getValue(x + n, y, 0) \
    - grid.getValue(x, y + n, 0) \
    + grid.getValue(x + n, y + n, 0)

def part1() -> None:
  print('serial:', serial)
  r = -10000
  rx, ry = -1, -1
  for x in range(MIN, MAX - 2):
    for y in range(MIN, MAX - 2):
      ri = getPowerSquare(x, y, serial)
      if ri > r:
        r = ri
        rx = x
        ry = y
  assert rx != -1 and ry != -1, 'did not find answer'
  print('value:', r)
  print('%d,%d' % (rx, ry))

def part2() -> None:
  print('serial:', serial)

  # Preprocess into a grid that stores the sum of powers in the
  # lower-right rectangle anchored at (x, y).
  grid = ArrayGrid(MAX + 1, MAX + 1)
  for x in range(MAX, MIN - 1, -1):
    for y in range(MAX, MIN - 1, -1):
      p = getPower(x, y, serial)
      if x == MAX and y == MAX:
        v = p
      elif x == MAX:
        v = p + grid.getValue(x, y + 1)
      elif y == MAX:
        v = p + grid.getValue(x + 1, y)
      else:
        v = p + grid.getValue(x, y + 1) + grid.getValue(x + 1, y) - grid.getValue(x + 1, y + 1)
      grid.setValue(x, y, v)

  r = -10000
  rx, ry, rn = -1, -1, -1
  for x in range(MIN, MAX + 1):
    for y in range(MIN, MAX + 1):
      for n in range(1, 300 - max(x, y) + 1):
        ri = getPowerSquareFromGrid(grid, x, y, n)
        if ri > r:
          r = ri
          rx, ry, rn = x, y, n
  assert rx != -1 and ry != -1 and rn != -1, 'did not find answer'
  print('value:', r)
  print('%d,%d,%d' % (rx, ry, rn))

part2()
