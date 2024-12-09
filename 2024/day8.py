from common.sparsegrid import SparseGrid
from collections import defaultdict
from itertools import combinations

input = open('day8.txt').read().splitlines()

Coords = tuple[int, int]
Anntennas = dict[str, list[Coords]]

def parseInput() -> tuple[SparseGrid, Anntennas]:
  grid = SparseGrid.gridFrom2DInput(input, lambda c: c if c != '.' else None)
  print('grid:', grid.getMinCoords(), grid.getMaxCoords())

  antennas: dict[str, list[Coords]] = defaultdict(list)
  for pos in grid.getAllCoords():
    assert len(pos) == 2, 'bad SparseGrid coords'
    v = grid.getValue(pos)
    antennas[v].append(pos)

  print('antennas:', len(antennas))
  return grid, antennas

def part1() -> None:
  grid, antennas = parseInput()

  antinodes = set()
  for ant in antennas:
    for p1, p2 in combinations(antennas[ant], 2):
      x1, y1 = p1
      x2, y2 = p2
      dx = x2 - x1
      dy = y2 - y1
      for newCoords in [(x1 - dx, y1 - dy), (x2 + dx, y2 + dy)]:
        if grid.areCoordsWithinBounds(newCoords):
          antinodes.add(newCoords)

  print(len(antinodes))

def part2() -> None:
  grid, antennas = parseInput()

  antinodes = set()
  for ant in antennas:
    for p1, p2 in combinations(antennas[ant], 2):
      x1, y1 = p1
      x2, y2 = p2
      dx = x2 - x1
      dy = y2 - y1

      i = 0
      while grid.areCoordsWithinBounds((newCoords := (x1 - i * dx, y1 - i * dy))):
        antinodes.add(newCoords)
        i += 1

      i = 0
      while grid.areCoordsWithinBounds((newCoords := (x2 + i * dx, y2 + i * dy))):
        antinodes.add(newCoords)
        i += 1

  print(len(antinodes))

part2()
