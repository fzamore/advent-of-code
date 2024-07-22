from common.arraygrid import ArrayGrid
from collections import defaultdict

input = open('day18.txt').read().splitlines()

def initGrid() -> ArrayGrid:
  w, h = len(input[0]), len(input)
  print('dimensions', w, h)
  grid = ArrayGrid.gridFromInput(input)
  return grid

# Returns a count of each type of cell adjacent to the given cell.
def countAdjacent(grid: ArrayGrid, x: int, y: int) -> dict[str, int]:
  d: dict[str, int] = defaultdict(int)
  for nx, ny in grid.getAdjacentCoords(x, y, includeDiagonals=True):
    d[grid.getValue(nx, ny)] += 1
  return d

# Iterates the given cell and returns the new value.
def iterCell(grid: ArrayGrid, x: int, y: int) -> str:
  adj = countAdjacent(grid, x, y)
  def c(v):
    return adj.get(v, 0)

  match grid.getValue(x, y):
    case '.':
      return '|' if c('|') >= 3 else '.'
    case '|':
      return '#' if c('#') >= 3 else '|'
    case '#':
      return '#' if c('|') >= 1 and c('#') >= 1 else '.'
    case _:
      assert False, 'bad grid value'

def iterGrid(grid: ArrayGrid) -> ArrayGrid:
  w, h = grid.getWidth(), grid.getHeight()
  ngrid = ArrayGrid(w, h)
  for x in range(w):
    for y in range(h):
      ngrid.setValue(x, y, iterCell(grid, x, y))
  return ngrid

def computeScore(grid: ArrayGrid) -> int:
  d: dict[str, int] = defaultdict(int)
  w, h = grid.getWidth(), grid.getHeight()
  for x in range(w):
    for y in range(h):
      d[grid.getValue(x, y)] += 1

  return d['#'] * d['|']

def part1() -> None:
  grid = initGrid()
  grid.print2D()

  n = 10
  for _ in range(n):
    grid = iterGrid(grid)
  grid.print2D()

  print(computeScore(grid))

def part2() -> None:
  grid = initGrid()

  # We iterate the grid until we find a pattern, and extrapolate that to
  # find the score at the desired iteration.
  scoreToIteration: dict[int, int] = {}
  iterationToScore = {}

  patternStart = 503 # Found by experimentation.
  cycleLen = -1
  i = 0
  while True:
    grid = iterGrid(grid)
    score = computeScore(grid)
    if score in scoreToIteration and i >= patternStart:
      diff = i - scoreToIteration[score]
      # The condition for the cycle was found by experimentation.
      if diff == 2:
        print('cycle info:', i, score, scoreToIteration[score], i - scoreToIteration[score])
        if i != patternStart:
          # We've found the cycle length (in my case, this is 28).
          cycleLen = i - patternStart
          break

    scoreToIteration[score] = i
    iterationToScore[i] = score
    i += 1

  print()

  assert cycleLen != -1, 'did not find cycleLen'
  print('patternStart:', patternStart)
  print('cycleLen:', cycleLen)

  target = 1000000000 - 1
  targetWithinPattern = patternStart + ((target - patternStart) % cycleLen)
  print('targetWithinPattern:', targetWithinPattern)
  print(iterationToScore[targetWithinPattern])

part2()
