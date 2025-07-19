from common.arraygrid import ArrayGrid

data = open('day18.txt').read().splitlines()

def step(grid: ArrayGrid) -> ArrayGrid:
  w, h = grid.getWidth(), grid.getHeight()
  ngrid = ArrayGrid(w, h)
  for x, y, v in grid.getItems():
    on = 0
    for ax, ay in grid.getAdjacentCoords(x, y, includeDiagonals=True):
      if grid.getValue(ax, ay) == '#':
        on += 1
    if v == '#':
      nv = '#' if on in (2, 3) else '.'
    else:
      assert v == '.', 'bad grid value'
      nv = '#' if on == 3 else '.'
    ngrid.setValue(x, y, nv)
  return ngrid

def part1() -> None:
  grid = ArrayGrid.gridFromInput(data)
  print('input:', grid.getWidth(), grid.getHeight())
  n = 100
  for _ in range(n):
    grid = step(grid)
  print(sum(1 for e in grid.getItems() if e[2] == '#'))

part1()
