from common.arraygrid import ArrayGrid

data = open('day18.txt').read().splitlines()

Coords = tuple[int, int]

def step(grid: ArrayGrid, alwaysOn: list[Coords] = []) -> ArrayGrid:
  w, h = grid.getWidth(), grid.getHeight()
  ngrid = ArrayGrid(w, h)
  for x, y, v in grid.getItems():
    if (x, y) in alwaysOn:
      assert v == '#', 'alwaysOn failed'
      ngrid.setValue(x, y, '#')
      continue
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

def iterateAll(grid, alwaysOn: list[Coords] = [], n: int = 100) -> int:
  for _ in range(n):
    grid = step(grid, alwaysOn)
  return sum(1 for e in grid.getItems() if e[2] == '#')

def part1() -> None:
  grid = ArrayGrid.gridFromInput(data)
  print('input:', grid.getWidth(), grid.getHeight())
  print(iterateAll(grid))

def part2() -> None:
  grid = ArrayGrid.gridFromInput(data)
  w, h, = grid.getWidth(), grid.getHeight()
  print('input:', w, h)
  alwaysOn = [
    (0, 0),
    (0, h - 1),
    (w - 1, 0),
    (w - 1, h - 1),
  ]
  for x, y in alwaysOn:
    grid.setValue(x, y, '#')

  print(iterateAll(grid, alwaysOn))

part2()
