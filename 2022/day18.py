from common.sparsegrid import SparseGrid

input = open('day18.txt').read().splitlines()

def part1():
  grid = SparseGrid(3)
  values = []
  for line in input:
    x, y, z = map(int, line.split(','))
    values.append((x, y, z))
    grid.setValue((x, y, z), 1)

  deltas = [
    (0, 0, 1),
    (0, 0, -1),
    (0, 1, 0),
    (0, -1, 0),
    (1, 0, 0),
    (-1, 0, 0),
  ]
  count = 0
  for x, y, z in values:
    for dx, dy, dz in deltas:
      if not grid.hasValue((x + dx, y + dy, z + dz)):
        count += 1
  print(count)

part1()
