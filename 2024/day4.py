from common.arraygrid import ArrayGrid

input = open('day4.txt').read().splitlines()

def isMatch(grid: ArrayGrid, x: int, y: int, dx: int, dy: int) -> bool:
  s = ('X', 'M', 'A', 'S')
  for i, v in enumerate(s):
    nx, ny = x + i * dx, y + i * dy
    if grid.getValue(nx, ny, '.') != v:
      return False
  return True

def isMatch2(grid: ArrayGrid, x: int, y: int) -> bool:
  # This pattern is centered on 'A'.
  if grid.getValue(x, y) != 'A':
    return False

  # All four orientations of the pattern we're looking for. Each entry is
  # deltas for 'M', 'M', 'S', 'S', (in that order).
  config = [
    ((-1, -1), (1, -1), (-1, 1), (1, 1)), # NW, NE; SW, SE
    ((-1, -1), (-1, 1), (1, 1), (1, -1)), # NW, SW; SE, NE
    ((-1, 1), (1, 1), (-1, -1), (1, -1)), # SW, SE; NE, NW
    ((1, 1), (1, -1), (-1, -1), (-1, 1)), # SE, NE; NW, SW
  ]

  for c in config:
    (m1dx, m1dy), (m2dx, m2dy), (s1dx, s1dy), (s2dx, s2dy) = c
    if grid.getValue(x + m1dx, y + m1dy, '.') == 'M' and \
        grid.getValue(x + m2dx, y + m2dy, '.') == 'M' and \
        grid.getValue(x + s1dx, y + s1dy, '.') == 'S' and \
        grid.getValue(x+ s2dx, y + s2dy, '.') == 'S':
      return True

  return False

def part1() -> None:
  grid = ArrayGrid.gridFromInput(input)
  width, height = grid.getWidth(), grid.getHeight()
  print('grid:', width, height)

  # Try all eight radial directions.
  deltas = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
     (-1, 1), (0, 1), (1, 1),
  ]

  ans = 0
  for y in range(height):
    for x in range(width):
      for dx, dy in deltas:
        if isMatch(grid, x, y, dx, dy):
          ans += 1
  print(ans)

def part2() -> None:
  grid = ArrayGrid.gridFromInput(input)
  width, height = grid.getWidth(), grid.getHeight()
  print('grid:', width, height)

  ans = 0
  for y in range(height):
    for x in range(width):
      if isMatch2(grid, x, y):
        ans += 1
  print(ans)

part2()
