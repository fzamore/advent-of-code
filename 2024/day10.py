from typing import Iterator
from common.arraygrid import ArrayGrid
from common.graphtraversal import dfs

input = open('day10.txt').read().splitlines()

Coords = tuple[int, int]

def getAdjacentNodes(grid: ArrayGrid, pos: Coords) -> Iterator[Coords]:
  x, y = pos
  v = grid.getValue(x, y)
  for ax, ay in grid.getAdjacentCoords(x, y):
    if grid.getValue(ax, ay) == v + 1:
      yield ax, ay

def findTrailheads(grid: ArrayGrid) -> set[Coords]:
  trailheads = set()
  def f(x: int, y: int, v: int):
    if v == 0:
      trailheads.add((x, y))
  grid.iterate(f)
  return trailheads

def getTrailheadScore(grid: ArrayGrid, trailhead: Coords) -> int:
  score = 0
  def visit(pos: Coords) -> None:
    nonlocal score
    x, y = pos
    if grid.getValue(x, y) == 9:
      score += 1

  dfs(trailhead, lambda pos: getAdjacentNodes(grid, pos), set(), visit)
  return score

def getTrailheadRating(grid: ArrayGrid, pos: Coords) -> int:
  x, y = pos
  if grid.getValue(x, y) == 9:
    return 1

  return sum([getTrailheadRating(grid, apos) for apos in getAdjacentNodes(grid, pos)])

def part1() -> None:
  grid = ArrayGrid.gridFromInput(input, lambda v: int(v))
  w, h = grid.getWidth(), grid.getHeight()
  print('grid:', w, h)

  trailheads = findTrailheads(grid)
  print('trailheads:', len(trailheads))

  total = sum([getTrailheadScore(grid, th) for th in trailheads])
  print(total)

def part2() -> None:
  grid = ArrayGrid.gridFromInput(input, lambda v: int(v))
  w, h = grid.getWidth(), grid.getHeight()
  print('grid:', w, h)

  trailheads = findTrailheads(grid)
  print('trailheads:', len(trailheads))

  total = sum([getTrailheadRating(grid, th) for th in trailheads])
  print(total)

part2()
