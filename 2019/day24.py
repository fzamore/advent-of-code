from common.arraygrid import ArrayGrid

input = open('day24.txt').read().splitlines()

def advance(grid: ArrayGrid) -> ArrayGrid:
  w, h = grid.getWidth(), grid.getHeight()
  ngrid = ArrayGrid(w, h)
  for y in range(h):
    for x in range(w):
      c = len([1 for (nx, ny) in grid.getAdjacentCoords(x, y) \
               if grid.getValue(nx, ny) == '#'])
      if grid.getValue(x,y) == '#':
        v = '#' if c == 1 else '.'
      else:
        v = '#' if c in [1, 2] else '.'
      ngrid.setValue(x,y,v)
  return ngrid

def score(grid: ArrayGrid) -> int:
  p = 1
  s = 0
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      if grid.getValue(x,y) == '#':
        s += p
      p *= 2
  return s

def part1():
  grid = ArrayGrid.gridFromInput(input)
  grid.print2D()

  grids = set()
  while grid not in grids:
    grids.add(grid)
    grid = advance(grid)

  print('done')
  grid.print2D()
  print(score(grid))

part1()
