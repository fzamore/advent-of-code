from typing import Iterable
from common.arraygrid import ArrayGrid
from common.graphtraversal import bfs
from itertools import combinations, pairwise, permutations

input = open('day24.txt').read().splitlines()

Coords = tuple[int, int]

def getShortestPathLen(grid: ArrayGrid, c1: Coords, c2: Coords) -> int:
  def getAdj(c: Coords) -> Iterable[Coords]:
    x, y = c
    for ax, ay in grid.getAdjacentCoords(x, y):
      if grid.getValue(ax, ay) != '#':
        yield ax, ay

  def isDone(c: Coords) -> bool:
    return c == c2

  r = bfs(c1, getAdj, isEndNode=isDone)
  return r[c2]

def findWaypoints(grid: ArrayGrid) -> dict[str, Coords]:
  waypoints = {}
  for x, y in grid.getAllCoords():
    if (v := grid.getValue(x, y)) not in ['.', '#']:
      waypoints[v] = (x, y)
  return waypoints

def computePairwiseShortestPaths(
  grid: ArrayGrid,
  waypoints: dict[str, Coords],
) -> dict[tuple[Coords, Coords], int]:

  d = {}
  for n1, n2 in combinations(waypoints.values(), 2):
    p = getShortestPathLen(grid, n1, n2)
    d[(n1, n2)] = p
    d[(n2, n1)] = p
  return d

def getOrderings(waypoints: dict[str, Coords]) -> Iterable[tuple]:
  for ordering in permutations(waypoints.values()):
    if ordering[0] == waypoints['0']:
      # We consider this ordering only if it begins at the start.
      yield ordering

def part1() -> None:
  grid = ArrayGrid.gridFromInput(input)
  print('size:', grid.getWidth(), grid.getHeight())

  waypoints = findWaypoints(grid)
  print('waypoints:', len(waypoints))

  d = computePairwiseShortestPaths(grid, waypoints)

  def pathlen(ordering):
    return sum([d[c1, c2] for c1, c2 in pairwise(ordering)])

  ans = min([pathlen(o) for o in getOrderings(waypoints)])
  print(ans)

def part2() -> None:
  grid = ArrayGrid.gridFromInput(input)
  print('size:', grid.getWidth(), grid.getHeight())

  waypoints = findWaypoints(grid)
  print('waypoints:', len(waypoints))

  d = computePairwiseShortestPaths(grid, waypoints)

  def pathlen(ordering):
    return sum([d[c1, c2] for c1, c2 in pairwise(ordering)])

  # Add the start at the end of each ordering.
  ans = min([pathlen(o + (waypoints['0'],)) for o in getOrderings(waypoints)])
  print(ans)

part2()
