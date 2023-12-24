from itertools import combinations

input = open('day24.txt').read().splitlines()

Coords = tuple[int, int, int]
Deltas = tuple[int, int, int]
Intersection = tuple[float, float, float]

Stone = tuple[Coords, Deltas]

def parseInput() -> list[Stone]:
  result: list[Stone] = []
  for line in input:
    v = line.split( ' @ ')
    x, y, z = map(int, v[0].split(', '))
    dx, dy, dz = map(int, v[1].split(', '))
    assert dx != 0 and dy != 0 and dz != 0, 'no zeroes allowed in velocity'
    result.append(((x, y, z), (dx, dy, dz)))
  return result

def areStonesParallel(s1: Stone, s2: Stone) -> bool:
  _, (dx1, dy1, _) = s1
  _, (dx2, dy2, _) = s2

  return dx1 * dy2 == dy1 * dx2

def findIntersection(s1: Stone, s2: Stone) -> Intersection:
  (x1, y1, _), (dx1, dy1, _) = s1
  (x2, y2, _), (dx2, dy2, _) = s2
  b1 = y1 - x1 * dy1 / dx1
  b2 = y2 - x2 * dy2 / dx2

  xi = (b2 - b1) / (dy1 / dx1 - dy2 / dx2)
  yi = xi * dy1 / dx1 + b1

  return (xi, yi, 0)

def isIntersectionInPast(s: Stone, ix: Intersection) -> bool:
  (x, y, _), (dx, dy, _) = s
  xi, yi, _ = ix
  return (xi - x) / dx < 0 or (yi - y) / dy < 0

def part1() -> None:
  stones = parseInput()
  print(stones)
  print('stones:', len(stones))

  minPos = 200000000000000
  maxPos = 400000000000000

  valid = []
  for s1, s2 in combinations(stones, 2):
    print()
    print('comparing:', s1, s2)
    if areStonesParallel(s1, s2):
      print('parallel')
      continue

    xi, yi, _ = findIntersection(s1, s2)
    if isIntersectionInPast(s1, (xi, yi, 0)):
      print('s1 intersection in past')
      continue

    if isIntersectionInPast(s2, (xi, yi, 0)):
      print('s2 intersection in past')
      continue

    if not minPos <= xi <= maxPos or not minPos <= yi <= maxPos:
      print('intersection outside of range')
      continue

    print('ix: (%f, %f)' % (xi, yi))
    valid.append((s1, s2, (xi, yi)))
  print()
  print(len(valid))

part1()
