from typing import Iterator
from common.arraygrid import ArrayGrid

input = open('day21.txt').read().splitlines()

Rules = dict[ArrayGrid, ArrayGrid]

def buildGrid(grid: ArrayGrid, spec: str) -> None:
  x, y = 0, 0
  for c in spec:
    if c == '/':
      x = 0
      y += 1
      continue
    grid.setValue(x, y, c)
    x += 1

# Takes a rule spec and returns an input grid and output grid.
def initBaseGrids(rule: str) -> tuple[ArrayGrid, ArrayGrid]:
  match len(rule):
    case 20:
      size = 2
    case 34:
      size = 3
    case _:
      assert False, 'bad rule'

  ispec, ospec = rule.split(' => ')

  igrid = ArrayGrid(size, size)
  buildGrid(igrid, ispec)

  ogrid = ArrayGrid(size + 1, size + 1)
  buildGrid(ogrid, ospec)
  return igrid, ogrid

def rotateGridCW(grid: ArrayGrid) -> ArrayGrid:
  size = grid.getWidth()
  ngrid = ArrayGrid(size, size)
  for y in range(size):
    for x in range(size):
      nx = size - 1 - y
      ny = x
      ngrid.setValue(nx, ny, grid.getValue(x, y))
  return ngrid

def flipGridHorizontal(grid: ArrayGrid) -> ArrayGrid:
  size = grid.getWidth()
  ngrid = ArrayGrid(size, size)

  for y in range(size):
    for x in range(size):
      nx = size - 1 - x
      ngrid.setValue(nx, y, grid.getValue(x, y))
  return ngrid

# Expand the given grid into all possible variants (all four rotations,
# and flipping horizontal in each rotation), and deduping the result.
def expandGrid(grid: ArrayGrid) -> set[ArrayGrid]:
  grids = {grid, flipGridHorizontal(grid)}
  for _ in range(3):
    ngrid = rotateGridCW(grid)
    grids.add(ngrid)
    grids.add(flipGridHorizontal(ngrid))
    grid = ngrid
  return grids

def splitIntoSubgrids(grid: ArrayGrid, subsize: int) -> Iterator[tuple[ArrayGrid, int, int]]:
  n = grid.getWidth() // subsize
  for y in range(n):
    for x in range(n):
      subgrid = ArrayGrid(subsize, subsize)
      sx, sy = x * subsize, y * subsize
      for i in range(subsize):
        for j in range(subsize):
          subgrid.setValue(j, i, grid.getValue(sx + j, sy + i))
      yield subgrid, sx, sy

def iterate(grid: ArrayGrid, rules: Rules) -> ArrayGrid:
  size = grid.getWidth()
  if size % 2 == 0:
    subsize = 2
  elif size % 3 == 0:
    subsize = 3
  else:
    assert False, 'bad grid size'

  nsize = (size // subsize) * (subsize + 1)
  print('nsize/subsize:', nsize, subsize)
  ngrid = ArrayGrid(nsize, nsize)

  # Iterate through each subgrid and expand it into a new single larger grid.
  for subgrid, x, y in splitIntoSubgrids(grid, subsize):
    # Output grid.
    ogrid = rules[subgrid]
    assert ogrid.getWidth() == subsize + 1, 'bad output grid size'
    for i in range(subsize + 1):
      ny = y + i + y // subsize
      for j in range(subsize + 1):
        nx = x + j + x // subsize
        ngrid.setValue(nx, ny, ogrid.getValue(j, i))
  return ngrid

def countOn(grid: ArrayGrid) -> int:
  ans = 0
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      if grid.getValue(x, y) == '#':
        ans += 1
  return ans

def iterateN(n: int) -> int:
  print('rules:', len(input))

  grid = ArrayGrid(3, 3)
  buildGrid(grid, '.#./..#/###')
  grid.print2D()

  rules = {}
  for line in input:
    igrid, ogrid = initBaseGrids(line)
    grids = expandGrid(igrid)
    for g in grids:
      assert g not in rules, 'duplicate grid encountered in single expansion'
      rules[g] = ogrid

  print('rules after expansion:', len(rules))

  for i in range(n):
    grid = iterate(grid, rules)
    print('after iter:', i, countOn(grid))

  return countOn(grid)

def part1() -> None:
  print(iterateN(5))

def part2() -> None:
  print(iterateN(18))

part1()
