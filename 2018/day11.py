serial = int(open('day11.txt').read())

MIN = 1
MAX = 300

def getPower(x: int, y: int, serial: int) -> int:
  rackID = x + 10
  power = (rackID * y + serial) * rackID
  return (power // 100) % 10 - 5

def getPowerGrid(x: int, y: int, serial: int) -> int:
  s = 0
  for xi in range(x, x + 3):
    for yi in range(y, y + 3):
      assert MIN <= x <= MAX, 'bad x'
      assert MIN <= y <= MAX, 'bad y'
      s += getPower(xi, yi, serial)
  return s

def part1() -> None:
  print('serial:', serial)
  r = -10000
  rx, ry = -1, -1
  for x in range(MIN, MAX - 2):
    for y in range(MIN, MAX - 2):
      ri = getPowerGrid(x, y, serial)
      if ri > r:
        r = ri
        rx = x
        ry = y
  assert rx != -1 and ry != -1, 'did not find answer'
  print('value:', r)
  print('%d,%d' % (rx, ry))


part1()
