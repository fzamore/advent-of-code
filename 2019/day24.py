from common.arraygrid import ArrayGrid
from common.sparsegrid import SparseGrid

input = open('day24.txt').read().splitlines()

N = 5 # square grid dimension
M = N // 2 # midpoint coordinate

# Given a current value (either 1 or 0) and adjacent count, return the
# value in the next iteration.
def newValue(currentValue: int, adjacentCount: int) -> int:
  assert currentValue in [0, 1], 'bad currentValue'
  assert adjacentCount >= 0, 'adjacentCount must be non-negative'
  if currentValue == 1:
    return 1 if adjacentCount == 1 else 0
  else:
    return 1 if adjacentCount in [1, 2] else 0

def advance(grid: ArrayGrid) -> ArrayGrid:
  w, h = grid.getWidth(), grid.getHeight()
  ngrid = ArrayGrid(w, h)
  for y in range(h):
    for x in range(w):
      c = sum([grid.getValue(nx, ny) for (nx, ny) in grid.getAdjacentCoords(x, y)])
      nv = newValue(grid.getValue(x, y), c)
      ngrid.setValue(x, y, nv)
  return ngrid

def score(grid: ArrayGrid) -> int:
  p = 1
  s = 0
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      if grid.getValue(x, y) == 1:
        s += p
      p *= 2
  return s

# Calculates the adjacent tiles to the given (x, y) position. Returns (x,
# y, levelOffset) tuple. The levelOffset of each tuple should be added to
# the current level.
def getAdjacentTiles2(x: int, y: int) -> list[tuple[int, int, int]]:
  assert not (x == M and y == M), 'cannot get adjacent of center tile'

  result = []

  # Each of the following code blocks (for north, east, south, and west),
  # is split up into three levels: outer, inner, and no change.

  # North
  if y == 0:
    result.append((M, M - 1, -1))
  elif x == M and y == M + 1:
    result.extend([(nx, N - 1, 1) for nx in range(N)])
  else:
    result.append((x, y - 1, 0))

  # East
  if x == N - 1:
    result.append((M + 1, M, -1))
  elif x == M - 1 and y == M:
    result.extend([(0, ny, 1) for ny in range(N)])
  else:
    result.append((x + 1, y, 0))

  # South
  if y == N - 1:
    result.append((M, M + 1, -1))
  elif x == M and y == M - 1:
    result.extend([(nx, 0, 1) for nx in range(N)])
  else:
    result.append((x, y + 1, 0))

  # West
  if x == 0:
    result.append((M - 1, M, -1))
  elif x == M + 1 and y == M:
    result.extend([(N - 1, ny, 1) for ny in range(N)])
  else:
    result.append((x - 1, y, 0))

  assert len(result) in [4, 8], 'bad adjacent result'
  return result

def advance2(grid: SparseGrid) -> SparseGrid:
  ngrid = SparseGrid(3)

  minlevel, maxlevel = grid.getMinCoords()[2], grid.getMaxCoords()[2]
  # Extend one level in each direction beyond what we currently have.
  minlevel -= 1
  maxlevel += 1

  print('advancing. min/max level:', minlevel, maxlevel)
  for level in range(minlevel, maxlevel + 1):
    for y in range(N):
      for x in range(N):
        if x == M and y == M:
          # Skip the center tile, as that will be handled recursively.
          continue

        count = 0
        for nx, ny, levelOffset in getAdjacentTiles2(x, y):
          if grid.hasValue((nx, ny, level + levelOffset)):
            count += 1

        if newValue(grid.getValue((x, y, level), 0), count) == 1:
          ngrid.setValue((x, y, level), 1)

    assert not ngrid.hasValue((M, M, level)), 'grid should not have value at midpoint'

  return ngrid

def printGrid(grid: SparseGrid) -> None:
  print()
  grid.print2DSlices(default='.', charMap = {1: '#'})

def part1() -> None:
  # Maintain an ArrayGrid of 1's and 0's.
  grid = ArrayGrid.gridFromInput(input, lambda s: 1 if s == '#' else 0)
  grid.print2D({1: '#', 0: '.'})

  grids = {grid}
  while (grid := advance(grid)) not in grids:
    grids.add(grid)

  print('done')
  grid.print2D({1: '#', 0: '.'})
  print(score(grid))

def part2() -> None:
  assert len(input) == N and len(input[0]) == N, 'bad input'
  # Maintain a single three-dimensional SparseGrid to represent the entire
  # state, where the z-coordinate is the grid-level (the initial grid is
  # level 0; each inner grid is +1, each outer grid is -1). The only value
  # that is ever added to the grid is 1, which represents a bug at that
  # cell. If there is no bug at that cell, there is no value in the grid.
  # This allows us to count the number of values within the grid to
  # determine the number of bugs (rather than inspecting the value of each
  # grid cell).
  grid = SparseGrid(3)

  for y in range(N):
    for x in range(N):
      v = input[y][x]
      if x == M and y == M:
        assert v == '.', 'center should be empty'
      if v == '#':
        grid.setValue((x, y, 0), 1)
  printGrid(grid)

  for _ in range(200):
    grid = advance2(grid)
  printGrid(grid)
  print(len(grid.getAllCoords()))

part2()
