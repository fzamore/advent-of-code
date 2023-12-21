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
  return grid, start

def canMove(
  grid: ArrayGrid,
  pos: tuple[int, int],
  delta: tuple[int, int],
) -> bool:
  x, y = pos
  dx, dy = delta
  return grid.getValue(x + dx, y + dy, '#') == '.'

def iterate(grid: ArrayGrid, points: set[tuple[int, int]]) -> set[tuple[int, int]]:
  result = set()
  deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
  for x, y in points:
    for dx, dy in deltas:
      if canMove(grid, (x, y), (dx, dy)):
        result.add((x + dx, y + dy))
  return result

def part1() -> None:
  grid, start = initGrid()
  grid.setValue(start[0], start[1], '.')
  grid.print2D()

  cur = set([start])
  for _ in range(64):
    cur = iterate(grid, cur)
  for x, y in cur:
    grid.setValue(x, y, 'O')
  grid.print2D()
  print(len(cur))

part1()
