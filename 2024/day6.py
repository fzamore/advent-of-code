from common.arraygrid import ArrayGrid

input = open('day6.txt').read().splitlines()

Coords = tuple[int, int]
Dir = tuple[int, int]

def findStart(grid: ArrayGrid) -> Coords:
  start = -1, -1
  def fn(x: int, y: int, v: str) -> None:
    nonlocal start
    if v == '^':
      start = x, y
  grid.iterate(fn)

  assert start != (-1, -1), 'did not find start'
  return start

def turnRight(dir: Dir) -> Dir:
  match dir:
    case 1, 0:
      return 0, 1
    case 0, 1:
      return -1, 0
    case -1, 0:
      return 0, -1
    case 0, -1:
      return 1, 0
    case _:
      assert False, 'bad dir'

def goStraight(grid: ArrayGrid, pos: Coords, dir: Dir) -> tuple[Coords, set[Coords]]:
  x, y = pos
  dx, dy = dir
  seen = {(x, y)}
  while grid.getValue(x + dx, y + dy, 'X') != '#':
    x += dx
    y += dy
    if not grid.areCoordsWithinBounds(x, y):
      break
    seen.add((x, y))
  return (x, y), seen

def iterate(grid: ArrayGrid, start: Coords, dir: Dir) -> set[Coords]:
  x, y = start
  totalSeen = set()
  while grid.areCoordsWithinBounds(x, y):
    (x, y), seen = goStraight(grid, (x, y), dir)
    totalSeen.update(seen)
    dir = turnRight(dir)
  return totalSeen

def part1() -> None:
  grid = ArrayGrid.gridFromInput(input)
  print('grid:', grid.getWidth(), grid.getHeight())
  start = findStart(grid)
  print('start:', start)

  totalSeen = iterate(grid, start, (0, -1))
  print(len(totalSeen))

part1()
