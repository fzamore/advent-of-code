from common.sparsegrid import SparseGrid

input = open('day19.txt').read().splitlines()

Coords = tuple[int, int]
Delta = tuple[int, int]

def findStart(grid: SparseGrid) -> Coords:
  x, y = 0, 0
  while not grid.hasValue((x, y)):
    x += 1
  return x, y

def getNextPosAndDir(grid: SparseGrid, pos: Coords, dir: Delta) -> tuple[Coords, Delta]:
  x, y = pos
  dx, dy = dir
  nx, ny = x + dx, y + dy
  npos = nx, ny
  if grid.getValue(pos) != '+' or grid.hasValue(npos):
    # Keep going straight unless we're at an intersection.
    return npos, dir

  # Try both orthogonal directions.
  nx1, ny1 = x + dy, y + dx
  nx2, ny2 = x - dy, y - dx

  npos1 = nx1, ny1
  npos2 = nx2, ny2

  if grid.hasValue(npos1):
    assert not grid.hasValue(npos2), 'multiple valid directions'
    return npos1, (dy, dx)

  if grid.hasValue(npos2):
    assert not grid.hasValue(npos1), 'multiple valid directions'
    return npos2, (-dy, -dx)

  assert False, 'no direction to turn'

def traverseGrid(grid: SparseGrid, pos: Coords, dir: Delta) -> list[Coords]:
  cells = []
  while grid.hasValue(pos):
    cells.append(pos)
    pos, dir = getNextPosAndDir(grid, pos, dir)
  return cells

def part1() -> None:
  grid = SparseGrid.gridFrom2DInput(input, lambda c: c if c != ' ' else None)
  start = findStart(grid)

  print('grid:', grid.getMinCoords(), grid.getMaxCoords())
  print('start:', start)

  cells = traverseGrid(grid, start, (0, 1))
  letters = [grid.getValue(c) for c in cells if grid.getValue(c) not in ['-', '|', '+']]
  print(''.join(letters))

def part2() -> None:
  grid = SparseGrid.gridFrom2DInput(input, lambda c: c if c != ' ' else None)
  start = findStart(grid)

  print('grid:', grid.getMinCoords(), grid.getMaxCoords())
  print('start:', start)

  cells = traverseGrid(grid, start, (0, 1))
  print(len(cells))

part2()
