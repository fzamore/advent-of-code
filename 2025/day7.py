from common.arraygrid import ArrayGrid
from functools import cache
import sys

data = open('day7.txt').read().splitlines()

sys.setrecursionlimit(300)

def parse() -> tuple[ArrayGrid, int, int]:
  grid = ArrayGrid.gridFromInput(data)
  for x, y, v in grid.getItems():
    if v == 'S':
      return grid, x, y
  assert False, 'did not find start'

@cache
def dfs(grid: ArrayGrid, x: int, y: int) -> int:
  assert 0 <= y < grid.getHeight(), 'bad y coordinate'
  if x < 0 or x >= grid.getWidth():
    # We've exited the grid laterally.
    return 0

  y += 1
  if y == grid.getHeight():
    # Exited the grid at the bottom. This is one path.
    return 1

  match grid.getValue(x, y):
    case '^':
      # Splitter.
      return dfs(grid, x - 1, y) + dfs(grid, x + 1, y)
    case '.':
      return dfs(grid, x, y)
    case _:
      assert False, 'bad grid entry'

def part1() -> None:
  grid, startx, starty = parse()
  print('grid:', grid.getWidth(), grid.getHeight())
  print('start:', startx, starty)

  # Keep track of the beams as a set, so we don't visit nodes more than once.
  beams = {(startx, starty)}
  splitters = set()
  while len(beams) > 0:
    x, y = beams.pop()
    assert 0 <= y < grid.getHeight(), 'bad y coordinate'
    if x < 0 or x >= grid.getWidth():
      # We've exited the grid laterally.
      continue

    y += 1
    if y == grid.getHeight():
      # We've gone past the bottom of the grid.
      continue

    match grid.getValue(x, y):
      case '^':
        splitters.add((x, y))
        beams.add((x - 1, y))
        beams.add((x + 1, y))
      case '.':
        beams.add((x, y))
      case _:
        assert False, 'bad grid value'

  print(len(splitters))

def part2() -> None:
  grid, startx, starty = parse()
  print('grid:', grid.getWidth(), grid.getHeight())
  print('start:', startx, starty)

  ans = dfs(grid, startx, starty)
  print(ans)

part2()
