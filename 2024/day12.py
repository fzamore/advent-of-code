from typing import Iterator
from common.arraygrid import ArrayGrid
from common.graphtraversal import dfs

input = open('day12.txt').read().splitlines()

Coords = tuple[int, int]
Delta = tuple[int, int]
Region = set[Coords]

def getAdjacentNodes(grid: ArrayGrid, pos: Coords) -> Iterator[Coords]:
  x, y = pos
  v = grid.getValue(x, y)
  for ax, ay in grid.getAdjacentCoords(x, y):
    if grid.getValue(ax, ay) == v:
      yield ax, ay

def getRegion(grid: ArrayGrid, start: Coords) -> Region:
  region = set()
  v = grid.getValue(start[0], start[1])
  def visit(pos: Coords) -> None:
    x, y = pos
    if grid.getValue(x, y) == v:
      region.add((x, y))

  dfs(start, lambda pos: getAdjacentNodes(grid, pos), visitNode=visit)
  return region

def findRegions(grid: ArrayGrid) -> list[Region]:
  regions = []
  pointsInAnyRegion = set()
  for pos in grid.getAllCoords():
    if pos in pointsInAnyRegion:
      continue

    region = getRegion(grid, pos)
    regions.append(region)
    pointsInAnyRegion.update(region)
  return regions

def getRegionArea(region: Region) -> int:
  return len(region)

def getRegionPerimeter(grid: ArrayGrid, region: Region) -> int:
  perim = 0
  for pos in region:
    adjCount = len(list(getAdjacentNodes(grid, pos)))
    perim += 4 - adjCount
  return perim

def getRegionValue(grid: ArrayGrid, region: Region) -> str:
  for x, y in region:
    return grid.getValue(x, y)
  assert False, 'empty region'

def getRegionSideCount(grid: ArrayGrid, region: Region) -> int:
  # This is kind of a mess. The approach is essentially to create
  # "mini"-sides for each point within the region, and then to "merge"
  # these mini-sides to form complete sides.
  #
  # We start by considering each point in the region, and adding an entry
  # for that point to the candidate set for each adjacent point that isn't
  # in the same region. So, each point could be added to the set a maximum
  # of four times (if it's a region of size 1), or a minimum of zero times
  # (if it's a completely interior point).
  #
  # Then, for each candidate, we consider it a new side, and then traverse
  # laterally in each of the two perpendicular directions to find all
  # points that are part of the same side. We remove each such (point,
  # delta) pair from our candidate set and repeat until we've considered
  # all candidates.

  value = getRegionValue(grid, region)
  candidates = set()
  for x, y in region:
    for ax, ay in grid.getAdjacentCoords(x, y, checkGridBounds=False):
      if grid.getValue(ax, ay, '.') != value:
        dx, dy = ax - x, ay - y
        assert (dx, dy) in {(1, 0), (0, 1), (-1, 0), (0, -1)}, 'bad delta'
        candidates.add(((x, y), (dx, dy)))

  count = 0
  while len(candidates) > 0:
    (x, y), (dx, dy) = candidates.pop()

    # We've encountered a new side of the region.
    count += 1

    # Next, we want to remove all candidates that are part of this same
    # side.

    # Traverse in each of the two perpendicular directions.
    perpendicularDeltas = [(1, 0), (-1, 0)] if dx == 0 else [(0, 1), (0, -1)]
    for ndx, ndy in perpendicularDeltas:
      # Continue traversing until we leave the region (i.e., we encounter
      # a convex corner) OR until we hit a point in the region that isn't
      # part of the same side (i.e., the point in the primary direction is
      # in the same region).
      nx, ny = x + ndx, y + ndy
      while (nx, ny) in region and (nx + dx, ny + dy) not in region:
        candidates.remove(((nx, ny), (dx, dy)))
        nx += ndx
        ny += ndy

  return count

def part1() -> None:
  grid = ArrayGrid.gridFromInput(input)
  print('grid:', grid.getWidth(), grid.getHeight())

  regions = findRegions(grid)
  print('regions:', len(regions))

  ans = 0
  for region in regions:
    ans += getRegionArea(region) * getRegionPerimeter(grid, region)
  print(ans)

def part2() -> None:
  grid = ArrayGrid.gridFromInput(input)
  print('grid:', grid.getWidth(), grid.getHeight())

  regions = findRegions(grid)
  print('regions:', len(regions))

  ans = 0
  for region in regions:
    ans += getRegionArea(region) * getRegionSideCount(grid, region)
  print(ans)

part2()

