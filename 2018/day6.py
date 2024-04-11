from typing import Iterator
from common.sparsegrid import SparseGrid
from collections import Counter

input = open('day6.txt').read().splitlines()

Coords = tuple[int, int]

def parseInput() -> list[Coords]:
  r = []
  for line in input:
    v = line.split(', ')
    r.append((int(v[0]), int(v[1])))
  return r

# Consider renaming this to getAdjacent2DCoordsInGrid and moving into SparseGrid.
def getAdjacentCoords(grid: SparseGrid, coords) -> Iterator[Coords]:
  x, y = coords
  for nx, ny in grid.getAdjacentCoordsInGrid(coords):
    if nx - x == 0 or ny - y == 0:
      yield nx, ny

def part1() -> None:
  coords = parseInput()
  print('coords:', len(coords))

  grid = SparseGrid(2)
  for x, y in coords:
    grid.setValue((x, y), '#')

  minCoords = grid.getMinCoords()
  maxCoords = grid.getMaxCoords()
  print('min/max:', minCoords, maxCoords)

  # Map each possible coordinate pair to the closest input coordinate pair.
  areas = {}
  for y in range(minCoords[1], maxCoords[1] + 1):
    for x in range(minCoords[0], maxCoords[0] + 1):
      minDist = float('inf')
      closestCoords = None
      for px, py in grid.getAllCoords():
        manHDist = abs(px - x) + abs(py - y)
        if manHDist < minDist:
          minDist = manHDist
          closestCoords = (px, py)
      assert closestCoords is not None, 'did not find closest coords'
      areas[x, y] = closestCoords

  areaSizes: dict[Coords, int] = Counter()
  infiniteAreas = set()
  for x, y in areas:
    rx, ry = areas[x, y]
    if x in [minCoords[0], maxCoords[0]] or y in [minCoords[1], maxCoords[1]]:
      # Skip infinite areas.
      infiniteAreas.add((rx, ry))
      continue
    areaSizes[rx, ry] += 1

  # Discard infinite areas.
  for x, y in infiniteAreas:
    del areaSizes[x, y]

  print(areaSizes)
  print(max(areaSizes.values()))

def part2() -> None:
  coords = parseInput()
  print('coords:', len(coords))

  threshold = 10000 if len(coords) == 50 else 32
  print('threshold:', threshold)

  grid = SparseGrid(2)
  for x, y in coords:
    grid.setValue((x, y), '#')

  minCoords = grid.getMinCoords()
  maxCoords = grid.getMaxCoords()
  print('min/max:', minCoords, maxCoords)

  total = 0
  for y in range(minCoords[1], maxCoords[1] + 1):
    for x in range(minCoords[0], maxCoords[0] + 1):
      totalDist = 0
      for px, py in grid.getAllCoords():
        manHDist = abs(px - x) + abs(py - y)
        totalDist += manHDist
      if totalDist < threshold:
        total += 1
  print(total)

part2()
