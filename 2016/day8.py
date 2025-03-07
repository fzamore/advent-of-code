from common.sparsegrid import SparseGrid
from common.ints import ints

input = open('day8.txt').read().splitlines()
width = 50
height = 6

Coords = tuple[int, int]

def rect(grid: SparseGrid, w: int, h: int) -> None:
  for x in range(w):
    for y in range(h):
      grid.setValue((x, y), '#')

def updateGrid(grid: SparseGrid, updates: dict[Coords, bool]) -> None:
  for x, y in updates:
    if updates[(x, y)]:
      grid.setValue((x, y), '#')
    else:
      grid.deleteValue((x, y))

def row(grid: SparseGrid, y: int, n: int) -> None:
  updates = {}
  for x in range(width):
    nx = (x + n) % width
    updates[(nx, y)] = grid.hasValue((x, y))
  updateGrid(grid, updates)

def col(grid: SparseGrid, x: int, n: int) -> None:
  updates = {}
  for y in range(height):
    ny = (y + n) % height
    updates[(x, ny)] = grid.hasValue((x, y))
  updateGrid(grid, updates)

def part1() -> None:
  grid = SparseGrid(2)

  for line in input:
    v = line.split()
    a, b = ints(line)
    if v[0] == 'rect':
      rect(grid, a, b)
    elif v[1] == 'row':
      row(grid, a, b)
    elif v[1] == 'column':
      col(grid, a, b)
    else:
      assert False, 'bad line'

  grid.print2D(default=' ')
  print(len(grid.getAllCoords()))

part1()
