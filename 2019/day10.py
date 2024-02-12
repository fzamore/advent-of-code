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

def countVisibleFromAsteroid(grid: SparseGrid, asteroid: Coords) -> int:
  count = 0
  for satellite in grid.getAllCoords():
    assert len(satellite) == 2, 'bad coords'
    if asteroid == satellite:
      continue
    if isVisibleFrom(grid, asteroid, satellite):
      count += 1
  return count

def part1() -> None:
  grid = SparseGrid.gridFrom2DInput(input, lambda v: v if v == '#' else None)
  grid.print2D(default='.')
  print('asteroids:', len(grid.getAllCoords()))

  maxCount = 0
  for asteroid in grid.getAllCoords():
    assert len(asteroid) == 2, 'bad coords: %s' % asteroid
    maxCount = max(maxCount, countVisibleFromAsteroid(grid, asteroid))
  print(maxCount)

part1()
