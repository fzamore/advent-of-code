from common.arraygrid import ArrayGrid

data = open('day4.txt').read().splitlines()

def canRemoveRoll(grid: ArrayGrid, x: int, y: int) -> bool:
  if grid.getValue(x, y) != '@':
    return False
  return sum(int(grid.getValue(ax, ay) == '@') for (ax, ay) in grid.getAdjacentCoords(x, y, includeDiagonals=True)) < 4

def iterate(grid: ArrayGrid) -> int:
  # First, find all rolls that can be removed.
  coords = [(x, y) for (x, y) in grid.getAllCoords() if canRemoveRoll(grid, x, y)]
  for x, y in coords:
    # Remove the rolls.
    grid.setValue(x, y, '.')

  # Return the number of rolls that were removed.
  return len(coords)

def part1() -> None:
  grid = ArrayGrid.gridFromInput(data)
  print('size:', grid.getWidth(), grid.getHeight())

  ans = sum(int(canRemoveRoll(grid, x, y)) for (x, y) in grid.getAllCoords())
  print(ans)

def part2() -> None:
  grid = ArrayGrid.gridFromInput(data)
  print('size:', grid.getWidth(), grid.getHeight())

  ans = 0
  while (v := iterate(grid)) > 0:
    ans += v
  print(ans)

part2()
