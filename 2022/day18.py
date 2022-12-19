input = open('day18.txt').read().splitlines()

def part1():
  points = set()
  for line in input:
    x, y, z = map(int, line.split(','))
    points.add((x, y, z))

  deltas = [
    (0, 0, 1),
    (0, 0, -1),
    (0, 1, 0),
    (0, -1, 0),
    (1, 0, 0),
    (-1, 0, 0),
  ]
  count = 0
  for x, y, z in points:
    for dx, dy, dz in deltas:
      if (x + dx, y + dy, z + dz) not in points:
        count += 1
  print(count)

def part2():
  MIN = 1000
  MAX = -1000
  points = set()
  for line in input:
    x, y, z = map(int, line.split(','))
    points.add((x, y, z))
    MIN = min(MIN, x, y, z)
    MAX = max(MAX, x, y, z)

  deltas = [
    (0, 0, 1),
    (0, 0, -1),
    (0, 1, 0),
    (0, -1, 0),
    (1, 0, 0),
    (-1, 0, 0),
  ]

  print('num points:', len(points))
  print('min:', MIN, 'max:', MAX)

  # Returns whether this point has a path to the outside. Also takes a
  # visited set, so we don't visit points we've already seen.
  def canEscape(
    point: tuple[int, int, int],
    visited: set[tuple[int, int, int]],
  ) -> bool:
    assert point not in points, 'bad point to canEscape'
    for c in point:
      if c < MIN or c > MAX:
        # We're free!
        return True
    x, y, z = point
    for dx, dy, dz in deltas:
      nx, ny, nz = x + dx, y + dy, z + dz
      if (nx, ny, nz) in visited:
        # We've already seen this point. Skip.
        continue
      # Mark this point as visied so we don't go back to it.
      visited.add((nx, ny, nz))
      if (nx, ny, nz) not in points:
        if canEscape((nx, ny, nz), visited):
          # We can escape from this direction. Stop.
          return True
    return False

  count = 0
  for x, y, z in points:
    for dx, dy, dz in deltas:
      nx, ny, nz = x + dx, y + dy, z + dz
      if (nx, ny, nz) not in points:
        # This point has a face not touching another point. Check whether
        # it can escape.
        if canEscape((nx, ny, nz), set()):
          count += 1

  print(count)

part2()
