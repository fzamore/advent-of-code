from typing import Any, Callable, Optional
from common.sparsegrid import SparseGrid

input = open('day3.txt').read()

Heading = tuple[int, int]
Coords = tuple[int, int]

# Returns the new heading given a left turn from the given heading.
def leftTurn(heading: Heading) -> Heading:
  match heading:
    case -1, 0:
      return 0, 1
    case 0, -1:
      return -1, 0
    case 1, 0:
      return 0, -1
    case 0, 1:
      return 1, 0
    case _:
      assert False

# Iterates through the given grid, starting at the third cell (assuming
# the first two cells have already been filled in). The first callback is
# to compute the value to store at that cell. The second callback returns
# None if the iteration isn't done, and returns a value if it is done (and
# `iterate` then returns that value).
def iterate(
  grid: SparseGrid,
  computeCellValue: Callable[[int, Coords], int],
  isDone: Callable[[int, Coords], Any],
) -> Any:
  # We assume we're starting from the third cell.
  assert grid.hasValue((0, 0)) and grid.hasValue((1, 0)), 'missing grid cells'
  pos = (1, 0)
  heading = (1, 0)
  step = 3
  while True:
    x, y = pos

    ndx, ndy = leftTurn(heading)
    nx, ny = x + ndx, y + ndy
    if not grid.hasValue((nx, ny)):
      # If we can turn left, do it.
      pos = nx, ny
      heading = ndx, ndy
    else:
      # Otherwise, keep going straight.
      dx, dy = heading
      pos = x + dx, y + dy
    value = computeCellValue(step, pos)
    grid.setValue(pos, value)
    result = isDone(step, pos)
    if result is not None:
      return result

    step += 1

def part1() -> None:
  target = int(input)
  print('target:', target)

  grid = SparseGrid(2)
  # Hardcode the first two cells.
  grid.setValue((0, 0), 1)
  grid.setValue((1, 0), 2)

  def computeCellValue(step: int, pos: Coords) -> int:
    return step

  def isDone(step: int, pos: Coords) -> Optional[Coords]:
    if step == target:
      return pos
    return None

  pos = iterate(grid, computeCellValue, isDone)

  print('pos:', pos)
  x, y = pos
  ans = abs(x) + abs(y)
  print(ans)

def part2() -> None:
  target = int(input)
  print('target:', target)

  grid = SparseGrid(2)
  # Hardcode the first two cells.
  grid.setValue((0, 0), 1)
  grid.setValue((1, 0), 1)

  def computeCellValue(step: int, pos: Coords) -> int:
    return sum([grid.getValue(x, 0) for x in grid.getAdjacentCoords(pos)])

  def isDone(step: int, pos: Coords) -> Optional[Coords]:
    value = grid.getValue(pos)
    if value > target:
      print('final pos:', pos)
      return value
    return None

  value = iterate(grid, computeCellValue, isDone)
  print(value)

part2()
