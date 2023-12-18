from common.sparsegrid import SparseGrid

input = open('day18.txt').read().splitlines()

def part1() -> None:
  deltas = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
  }

  grid = SparseGrid(2)
  cx, cy = 0, 0
  grid.setValue((cx, cy), '#')
  for line in input:
    values = line.split()
    dir = values[0]
    qty = int(values[1])
    dx, dy = deltas[dir]

    for _ in range(qty):
      cx += dx
      cy += dy
      grid.setValue((cx, cy), '#')

  grid.print2D(default='.')

  # Count interior spaces by shooting a ray across each row and flip
  # in/out when you hit a vertical wall.
  count = 0
  (mnx, mny), (mxx, mxy) = grid.getMinCoords(), grid.getMaxCoords()
  for y in range(mny, mxy):
    # Examine row between y and y + 1
    on = False
    for x in range(mnx - 1, mxx + 1):
      if grid.hasValue((x, y)) and grid.hasValue((x, y + 1)):
        # If we're crossing a vertical wall (indicated by existing values
        # in both rows of the grid), flip.
        on = not on
      if on and not grid.hasValue((x, y)):
        # We're inside the grid.
        count += 1
  print('count inside:', count)
  print('count on border:', len(grid.getAllCoords()))
  print(count + len(grid.getAllCoords()))

part1()

