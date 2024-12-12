from typing import Iterator
from common.arraygrid import ArrayGrid
from common.graphtraversal import dfs

input = open('day12.txt').read().splitlines()

Coords = tuple[int, int]

def getAdjacentNodes(grid: ArrayGrid, pos: Coords) -> Iterator[Coords]:
  x, y = pos
  v = grid.getValue(x, y)
  for ax, ay in grid.getAdjacentCoords(x, y):
    if grid.getValue(ax, ay) == v:
      yield ax, ay

def getRegion(grid: ArrayGrid, start: Coords) -> set[Coords]:
  region = set()
  v = grid.getValue(start[0], start[1])
  def visit(pos: Coords) -> None:
    x, y = pos
    if grid.getValue(x, y) == v:
      region.add((x, y))

  dfs(start, lambda pos: getAdjacentNodes(grid, pos), visitNode=visit)
  return region

def getRegionArea(region: set[Coords]) -> int:
  return len(region)

def getRegionPerimeter(grid: ArrayGrid, region: set[Coords]) -> int:
  perim = 0
  for pos in region:
    x, y = pos
    v = grid.getValue(x, y)
    adjCount = len(list(getAdjacentNodes(grid, pos)))
    perim += 4 - adjCount
  return perim

def part1() -> None:
  grid = ArrayGrid.gridFromInput(input)
  print('grid:', grid.getWidth(), grid.getHeight())

  regions = []
  pointsInAnyRegion = set()
  for pos in grid.getAllCoords():
    if pos in pointsInAnyRegion:
      continue

    region = getRegion(grid, pos)
    regions.append(region)
    pointsInAnyRegion.update(region)

  print('regions:', len(regions))

  ans = 0
  for region in regions:
    ans += getRegionArea(region) * getRegionPerimeter(grid, region)
  print(ans)

part1()

