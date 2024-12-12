from common.arraygrid import ArrayGrid

input = open('day6.txt').read().splitlines()

Coords = tuple[int, int]
Dir = tuple[int, int]

def findStart(grid: ArrayGrid) -> Coords:
  for x, y, v in grid.getItems():
    if v == '^':
      return (x, y)
  assert False, 'did not find start'

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
    for pos in seen:
      if (pos, dir) in totalSeen:
        # Returning an empty set indicates there was a loop.
        return set()
      totalSeen.add((pos, dir))
    dir = turnRight(dir)
  return set([pos for (pos, dir) in totalSeen])

def part1() -> None:
  grid = ArrayGrid.gridFromInput(input)
  print('grid:', grid.getWidth(), grid.getHeight())
  start = findStart(grid)
  print('start:', start)

  totalSeen = iterate(grid, start, (0, -1))
  print(len(totalSeen))

def part2() -> None:
  grid = ArrayGrid.gridFromInput(input)
  print('grid:', grid.getWidth(), grid.getHeight())
  start = findStart(grid)
  print('start:', start)

  dir = 0, -1
  totalSeen = iterate(grid, start, dir)

  ans = 0
  # Try each point in the path (since blockages in other points will have no effect).
  for x, y in totalSeen:
    grid.setValue(x, y, '#')
    if len(iterate(grid, start, dir)) == 0:
      # We found a loop.
      ans += 1
    grid.setValue(x, y, '.')
  print(ans)

part2()
