input = open('day11.txt').read().rstrip()

def getDelta(dir: str) -> tuple[int, int]:
  match dir:
    case 'n': return 0, -2
    case 'ne': return 1, -1
    case 'e': return 2, 0
    case 'se': return 1,1
    case 's': return 0, 2
    case 'sw': return -1, 1
    case 'w': return -2, 0
    case 'nw': return -1, -1
    case _: assert False, 'bad dir: %s' % dir

def getSteps(x: int, y: int) -> int:
  ax, ay = abs(x), abs(y)
  mn, mx = min(ax, ay), max(ax, ay)
  diff = mx - mn
  assert diff % 2 == 0
  return mn + diff // 2

def part1() -> None:
  dirs = input.split(',')
  print('dirs:', len(dirs))

  x, y = 0, 0
  for dir in dirs:
    dx, dy = getDelta(dir)
    x += dx
    y += dy
  print('end pos:', x, y)
  print(getSteps(x, y))

def part2() -> None:
  dirs = input.split(',')
  print('dirs:', len(dirs))

  mx = -1
  x, y = 0, 0
  for dir in dirs:
    dx, dy = getDelta(dir)
    x += dx
    y += dy
    mx = max(mx, getSteps(x, y))
  print(mx)

part2()
