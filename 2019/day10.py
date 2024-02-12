from math import gcd
from common.sparsegrid import SparseGrid

input = open('day10.txt').read().splitlines()

Coords = tuple[int, int]

def isVisibleFrom(grid: SparseGrid, base: Coords, satellite: Coords) -> bool:
  x, y = base
  sx, sy = satellite

  # We compute the x- and y-distances from base to satellite and want to
  # determine if there are any integer coordinates along the way. We use
  # the gcd of the x- and y-distances to compute how much to increment x
  # and y at each step.
  dx, dy = sx - x, sy - y
  factor = gcd(abs(dx), abs(dy))
  assert factor != 0, 'bad gcd'
  assert dx % factor == 0 and dy % factor == 0, 'bad gcd mod'
  dx, dy = dx // factor, dy // factor

  # We move from the base toward the satellite. If we reach the satellite
  # before reaching any other asteroid, it's visible.
  nx, ny = x + dx, y + dy
  while not grid.hasValue((nx, ny)):
    nx += dx
    ny += dy
  return nx == sx and ny == sy

def getVisibleFromAsteroid(grid: SparseGrid, asteroid: Coords) -> list[Coords]:
  visible = []
  for satellite in grid.getAllCoords():
    assert len(satellite) == 2, 'bad coords'
    if asteroid == satellite:
      continue
    if isVisibleFrom(grid, asteroid, satellite):
      visible.append(satellite)
  return visible

def asteroidKey(station: Coords, satellite: Coords) -> tuple[int, float]:
  x, y = station
  sx, sy = satellite
  dx, dy = sx - x, sy - y
  assert dx != 0 or dy != 0, 'dx and dy cannot both be zero'
  # Highest-order bit is quadrant, then slope (top-right quadrant is 1,
  # then increase clockwise). Return values should be in ascending order.
  # We treat vertical slopes as negative infinity, which means that
  # vertical slopes need to be the first entries in quadrants 1 and 3, and
  # not appear at all in quadrants 2 and 4.
  if dx >= 0 and dy < 0:
    quadrant = 1
  elif dx > 0 and dy >= 0:
    quadrant = 2
  elif dx <= 0 and dy >= 0:
    quadrant = 3
  elif dx < 0 and dy < 0:
    quadrant = 4
  else:
    assert False, 'bad quadrant math: %d, %d' % (dx, dy)
  slope = -float('inf') if dx == 0 else dy / dx
  return quadrant, slope

def part1() -> None:
  grid = SparseGrid.gridFrom2DInput(input, lambda v: v if v == '#' else None)
  grid.print2D(default='.')
  print('asteroids:', len(grid.getAllCoords()))

  maxCount = 0
  for asteroid in grid.getAllCoords():
    assert len(asteroid) == 2, 'bad coords: %s' % asteroid
    maxCount = max(maxCount, len(getVisibleFromAsteroid(grid, asteroid)))
  print(maxCount)

def part2() -> None:
  grid = SparseGrid.gridFrom2DInput(input, lambda v: v if v == '#' else None)
  grid.print2D(default='.')
  print('asteroids:', len(grid.getAllCoords()))

  maxCount = 0
  station = None
  for asteroid in grid.getAllCoords():
    assert len(asteroid) == 2, 'bad coords: %s' % asteroid
    count = len(getVisibleFromAsteroid(grid, asteroid))
    if count > maxCount:
      maxCount = count
      station = asteroid

  assert station is not None, 'did not find station'
  print('station:', station, maxCount)

  visible = getVisibleFromAsteroid(grid, station)
  visibleInOrder = sorted(visible, key=lambda x: asteroidKey(station, x))
  for i, x in enumerate(visibleInOrder):
    print('rank:', i + 1, x)

  # It turns out we never actually need to vaporize any asteroids, because
  # there are over 200 visible from the station.
  ans = visibleInOrder[199]
  print('200th:', ans)
  print(100 * ans[0] + ans[1])

part2()
