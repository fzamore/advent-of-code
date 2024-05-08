from common.sparsegrid import SparseGrid

input = open('day17.txt').read().splitlines()

Coords = tuple[int, int]

# Converts a line from a string like "x=504, y=10..13" to a list of coordinates.
def parseLine(line: str) -> list[Coords]:
  v = line.split(', ')
  assert len(v) == 2, 'bad line'

  coordA = int(v[0][2:])
  coordB1, coordB2 = map(int, v[1][2:].split('..'))
  assert coordB1 < coordB2, 'bad line'

  if v[0][0] == 'x':
    x1, x2 = coordA, coordA
    y1, y2 = coordB1, coordB2
  elif v[0][0] == 'y':
    x1, x2 = coordB1, coordB2
    y1, y2 = coordA, coordA
  else:
    assert False, 'bad line'

  r = []
  for y in range(y1, y2 + 1):
    for x in range(x1, x2 + 1):
      r.append((x, y))
  return r

def initGrid() -> SparseGrid:
  print('lines:', len(input))
  grid = SparseGrid(2)

  for line in input:
    for c in parseLine(line):
      grid.setValue(c, '#')
  return grid

# Starts the drip from the given source and fills the grid to entirety.
def drip(grid: SparseGrid, start: Coords, yMax: int) -> None:

  # Helper functions.
  def get(x: int, y: int) -> str:
    return grid.getValue((x, y), '.')
  def set(x: int, y: int, v: str) -> None:
    grid.setValue((x, y), v)

  q = [start]
  while len(q) > 0:
    x, y = q.pop()

    # Drop vertically until we hit something.
    while get(x, y) in ['.', '|'] and y <= yMax:
      set(x, y, '|')
      y += 1

    if y > yMax:
      # We've gone too far. Skip.
      continue

    assert get(x, y) in ['#', '~'], 'did not reach bottom'

    # Back up so we're at the last cell before the bottom.
    y -= 1

    # Keep track of cells in this row (either until we determine we're in
    # a basin or we can spill out over the edge).
    horizCells = [(x, y)]

    # Determine whether we're in a basin.
    inBasin = True

    # Traverse both left and right in this row.
    for dx in [-1, 1]:
      nx = x + dx
      while get(nx, y) != '#':
        set(nx, y, '|')
        horizCells.append((nx, y))
        # Check whether we can find a path to drip down.
        downValue = get(nx, y + 1)
        if downValue in ['.', '|']:
          # We found a spillover path. Stop traversing horizontally.
          if downValue == '.':
            # We haven't seen this path before, so add it to the queue.
            q.append((nx, y + 1))
          # Stop traversing horizontally and mark that we're not in a basin.
          inBasin = False
          break

        nx += dx

      assert get(nx, y) in ['|', '#'], 'bad basin edge computation'

    if inBasin:
      # If we're in a basin, mark all the cells we've seen in this row as at-rest.
      for hx, hy in horizCells:
        set(hx, hy, '~')

      # Add one cell above to our queue, so we can go back and mark the
      # corresponding row as at-rest. This can probably be done more
      # efficiently.
      q.append((x, y - 1))

def countCells(grid: SparseGrid, yMin: int, yMax: int, values: list[str]) -> int:
  count = 0
  for pos in grid.getAllCoords():
    _, y = pos
    if yMin <= y <= yMax and grid.getValue(pos) in values:
      count += 1
  return count

def part1() -> None:
  print()
  grid = initGrid()

  yMin = grid.getMinCoords()[1]
  yMax = grid.getMaxCoords()[1]

  print('min/max y values:', yMin, yMax)

  start = 500, 0
  drip(grid, start, yMax)

  grid.setValue(start, '+')
  grid.print2D(default='.')

  print(countCells(grid, yMin, yMax, ['|', '~']))

def part2() -> None:
  print()
  grid = initGrid()

  yMin = grid.getMinCoords()[1]
  yMax = grid.getMaxCoords()[1]

  print('min/max y values:', yMin, yMax)

  start = 500, 0
  drip(grid, start, yMax)

  grid.setValue(start, '+')
  grid.print2D(default='.')

  print(countCells(grid, yMin, yMax, ['~']))

part2()
