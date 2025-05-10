data = open('day3.txt').read().strip()

Coords = tuple[int, int]
Delta = tuple[int, int]

def getDelta(ch: str) -> Delta:
  assert len(ch) == 1, 'bad char'
  match ch:
    case '^': return 0, -1
    case '>': return 1, 0
    case 'v': return 0, 1
    case '<': return -1, 0
    case _: assert False, 'bad char'

def update(x: int, y: int, ch: str) -> Coords:
  dx, dy = getDelta(ch)
  return x + dx, y + dy

def part1() -> None:
  seen = set()
  x, y = 0, 0
  seen.add((x, y))
  for ch in data:
    x, y = update(x, y, ch)
    seen.add((x, y))
  print(len(seen))

def part2() -> None:
  seen = set()
  x1, y1, x2, y2 = 0, 0, 0, 0
  seen.add((x1, y1))
  for i in range(0, len(data), 2):
    ch1 = data[i]
    ch2 = data[i + 1]
    x1, y1 = update(x1, y1, ch1)
    x2, y2 = update(x2, y2, ch2)
    seen.add((x1, y1))
    seen.add((x2, y2))
  print(len(seen))

part2()
