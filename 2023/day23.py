from typing import Optional
from common.arraygrid import ArrayGrid

input = open('day23.txt').read().splitlines()

Coords = tuple[int, int]

def canMove(cur: Coords, next: Coords, nextValue: str) -> bool:
  allowed = {
    '<': (-1, 0),
    '>': (1, 0),
    'v': (0, 1),
    '^': (0, -1),
  }
  x, y = cur
  nx, ny = next
  dx, dy = nx - x, ny - y
  if nextValue == '.':
    return True
  elif nextValue == '#':
    return False

  return (dx, dy) == allowed[nextValue]

def getAdjacentCoords(
  grid: ArrayGrid,
  cur: Coords,
  prev: Optional[Coords],
  visited: set[Coords],
) -> list[Coords]:
  results = []
  x, y = cur
  for next in grid.getAdjacentCoords(x, y):
    if next == prev or next in visited:
      continue
    nx, ny = next
    if canMove(cur, next, grid.getValue(nx, ny)):
      results.append(next)
  return results

def findLongestPath(
  grid: ArrayGrid,
  cur: Coords,
  prev: Optional[Coords],
  end: Coords,
  visited: set[Coords] = set(),
) -> Optional[list[Coords]]:
  assert cur not in visited, 'already visited node: %s' % str(cur)
  visited.add(cur)
  path = [cur]

  # As long as there is exactly one way to go, keep moving that way
  # without recurring (to not increase the recursion stack depth).
  adj = getAdjacentCoords(grid, cur, prev, visited)
  while len(adj) == 1:
    prev = cur
    cur = adj[0]
    path.append(cur)
    visited.add(cur)
    adj = getAdjacentCoords(grid, cur, prev, visited)

  if cur == end:
    return path

  longestLen = -1
  longestPath = None
  for next in adj:
    npath = findLongestPath(grid, next, cur, end, visited.copy())
    if npath is None:
      continue
    if len(npath) > longestLen:
      longestLen = len(npath)
      longestPath = npath.copy()

  if longestPath is None:
    return None

  path.extend(longestPath)
  return path

def part1() -> None:
  grid = ArrayGrid.gridFromInput(input)
  w, h, = grid.getWidth(), grid.getHeight()
  print('grid: (%d x %d)' % (w, h))
  grid.print2D()

  start = (1, 0)
  end = (w - 2, h - 1)
  print('start:', start)
  print('end:', end)

  path = findLongestPath(grid, start, None, end)
  if path is not None:
    for x, y in path:
      v = 'S' if (x, y) == start else 'O'
      grid.setValue(x, y, v)
    grid.print2D()
    print(len(path) - 1)

part1()
