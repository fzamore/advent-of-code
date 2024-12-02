from common.sparsegrid import SparseGrid

input = open('day22.txt').read().splitlines()

Coords = tuple[int, int]
Delta = tuple[int, int]
Actions = dict[str, tuple[str, int]]

def iterate(grid: SparseGrid, pos: Coords, dir: Delta, actions: Actions) -> tuple[Coords, Delta]:
  cwdirs = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
  ]

  nv, dirdelta = actions[grid.getValue(pos, '.')]
  grid.setValue(pos, nv)

  dirpos = cwdirs.index(dir)
  assert dirpos >= 0, 'bad dirpos'

  ndir = cwdirs[(dirpos + dirdelta) % len(cwdirs)]
  dx, dy = ndir
  x, y = pos
  nx, ny = x + dx, y + dy
  return (nx, ny), ndir

# Iterates through N iterations and returns the number of cells that become infected.
def iterateN(grid: SparseGrid, n: int, actions: Actions) -> int:
  maxX, maxY = grid.getMaxCoords()
  print('grid max:', maxX, maxY)
  assert maxX % 2 == 0 and maxY % 2 == 0, 'bad input grid'

  pos = maxX // 2, maxY // 2
  dir = 0, -1
  print('start:', pos)

  infected = 0
  for _ in range(n):
    npos, dir = iterate(grid, pos, dir, actions)
    if grid.getValue(pos) == '#':
      infected += 1
    pos = npos

  return infected

def part1() -> None:
  grid = SparseGrid.gridFrom2DInput(input)
  actions = {
    '#': ('.', 1),
    '.': ('#', -1),
  }
  n = 10000
  print(iterateN(grid, n, actions))

def part2() -> None:
  grid = SparseGrid.gridFrom2DInput(input)
  actions = {
    '.': ('W', -1),
    'W': ('#', 0),
    '#': ('F', 1),
    'F': ('.', 2),
  }
  n = 10000000
  print(iterateN(grid, n, actions))

part2()
