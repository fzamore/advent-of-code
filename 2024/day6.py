from common.arraygrid import ArrayGrid, turnRight, Delta

input = open('day6.txt').read().splitlines()

Coords = tuple[int, int]

def findStart(grid: ArrayGrid) -> Coords:
  for x, y, v in grid.getItems():
    if v == '^':
      return (x, y)
  assert False, 'did not find start'

def goStraight(grid: ArrayGrid, pos: Coords, delta: Delta) -> tuple[Coords, set[Coords]]:
  x, y = pos
  dx, dy = delta
  seen = {(x, y)}
  while grid.getValue(x + dx, y + dy, 'X') != '#':
    x += dx
    y += dy
    if not grid.areCoordsWithinBounds(x, y):
      break
    seen.add((x, y))
  return (x, y), seen

def iterate(grid: ArrayGrid, start: Coords, delta: Delta) -> set[Coords]:
  x, y = start
  totalSeen = set()
  while grid.areCoordsWithinBounds(x, y):
    (x, y), seen = goStraight(grid, (x, y), delta)
    for pos in seen:
      if (pos, delta) in totalSeen:
        # Returning an empty set indicates there was a loop.
        return set()
      totalSeen.add((pos, delta))
    delta = turnRight(delta)
  return set([pos for (pos, _) in totalSeen])

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

  delta = 0, -1
  totalSeen = iterate(grid, start, delta)

  ans = 0
  # Try each point in the path (since blockages in other points will have no effect).
  for x, y in totalSeen:
    grid.setValue(x, y, '#')
    if len(iterate(grid, start, delta)) == 0:
      # We found a loop.
      ans += 1
    grid.setValue(x, y, '.')
  print(ans)

part2()
