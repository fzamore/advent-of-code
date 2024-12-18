from typing import Iterable
from common.arraygrid import ArrayGrid
from common.ints import ints
from common.shortestpath import dijkstra

input = open('day18.txt').read().splitlines()

Coords = tuple[int, int]

def parseInput(width: int, height: int, n: int) -> ArrayGrid:
  grid = ArrayGrid(width, height)
  for i in range(n):
    x, y = ints(input[i])
    grid.setValue(x, y, '#')
  return grid

def getAdjacent(grid: ArrayGrid, coords: Coords) -> Iterable[tuple[Coords, int]]:
  x, y = coords
  for ax, ay in grid.getAdjacentCoords(x, y):
    v = grid.getValue(ax, ay)
    if v != '#':
      yield (ax, ay), 1

def part1() -> None:
  # Values for sample input:
  # xMax, yMax = 6, 6
  # n = 12

  xMax, yMax = 70, 70
  n = 1024

  grid = parseInput(xMax + 1, yMax + 1, n)
  grid.print2D({None: '.'})

  start = 0,0
  end = xMax, yMax

  r = dijkstra(
    start,
    lambda p: getAdjacent(grid, p),
    lambda p: p == end,
  )
  print(r[1])

part1()
