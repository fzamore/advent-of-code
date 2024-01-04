from itertools import combinations
from z3 import Int, Solver, sat, unsat # type: ignore

input = open('day24.txt').read().splitlines()

Coords = tuple[float, float, float]
Velocities = tuple[float, float, float]

Stone = tuple[Coords, Velocities]

def parseInput() -> list[Stone]:
  result: list[Stone] = []
  for line in input:
    v = line.split( ' @ ')
    x, y, z = map(int, v[0].split(', '))
    dx, dy, dz = map(int, v[1].split(', '))
    assert dx != 0 and dy != 0 and dz != 0, 'no zeroes allowed in velocity'
    result.append(((x, y, z), (dx, dy, dz)))
  return result

def shouldCountStonePair(
  s1: Stone,
  s2: Stone,
  minPos: float,
  maxPos: float,
) -> bool:
  (x1, y1, _), (vx1, vy1, _) = s1
  (x2, y2, _), (vx2, vy2, _) = s2

  if vx1 * vy2 == vy1 * vx2:
    # Parallel stones.
    return False

  # Compute the intersection times.
  t1 = (vy2 * (x2 - x1) - vx2 * (y2 - y1)) / (vx1 * vy2 - vy1 * vx2)
  t2 = (vy1 * (x1 - x2) - vx1 * (y1 - y2)) / (vx2 * vy1 - vy2 * vx1)

  if t1 <= 0 or t2 <= 0:
    # Intersection not in the future.
    return False

  # Compute the intersection position.
  xi = x1 + vx1 * t1
  yi = y1 + vy1 * t1

  return minPos <= xi <= maxPos and minPos <= yi <= maxPos

def part1() -> None:
  stones = parseInput()
  print('stones:', len(stones))

  minPos = 200000000000000
  maxPos = 400000000000000

  # z3 is too slow for Part 1.
  count = 0
  for s1, s2 in combinations(stones, 2):
    if shouldCountStonePair(s1, s2, minPos, maxPos):
      count += 1

  print()
  print(count)

def part2() -> None:
  stones = parseInput()
  print('input stones:', len(stones))

  # z3 is a cheat code.
  solver = Solver()
  xi, yi, zi, vxi, vyi, vzi = map(Int, ['xi', 'yi', 'zi', 'vxi', 'vyi', 'vzi'])
  for i, stone in enumerate(stones):
    (x, y, z), (vx, vy, vz) = stone
    # Each intersection will occur at a different time, so we need a
    # different variable name for the time.
    t = Int('t%d' % (i + 1))
    solver.add(xi + vxi * t == x + vx * t)
    solver.add(yi + vyi * t == y + vy * t)
    solver.add(zi + vzi * t == z + vz * t)

  assert solver.check() == sat, 'could not find stone'
  model = solver.model()
  print(
    'found stone:',
    model[xi], model[yi], model[zi],
    model[vxi], model[vyi], model[vzi],
  )
  print()
  print(model.eval(xi + yi + zi))

part2()
