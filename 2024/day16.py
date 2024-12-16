from typing import Iterator
from common.shortestpath import dijkstra
from common.arraygrid import ArrayGrid

input = open('day16.txt').read().splitlines()

Coords = tuple[int, int]
Dir = tuple[int, int]
PosDir = tuple[Coords, Dir]

def parseInput() -> tuple[ArrayGrid, Coords, Coords]:
  start, end = None, None
  grid = ArrayGrid.gridFromInput(input)
  for x, y, v in grid.getItems():
    if v == 'S':
      start = x, y
    if v == 'E':
      end = x, y
  assert (start is not None) and (end is not None), 'did not find start and end'
  return grid, start, end

def getAdjacentNodes(grid: ArrayGrid, posdir: PosDir) -> Iterator[tuple[PosDir, int]]:
  (x, y), (dx, dy) = posdir
  for ax, ay in grid.getAdjacentCoords(x, y):
    adx, ady = ax - x, ay - y
    if adx == -dx and ady == -dy:
      # No u-turns allowed.
      continue

    av = grid.getValue(ax, ay)
    if av == '#':
      continue
    score = 1
    if (adx, ady) != (dx, dy):
      # Turning.
      score += 1000
    yield ((ax, ay), (adx, ady)), score

def part1() -> None:
  grid, start, end = parseInput()
  print('start/end:', start, end)

  startNode = start, (1, 0)
  r = dijkstra(startNode, lambda pd: getAdjacentNodes(grid, pd), lambda pd: pd[0] == end)
  print(r[1])

part1()
