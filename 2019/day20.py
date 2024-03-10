from typing import Any, Optional
from common.arraygrid import ArrayGrid
from collections import defaultdict
from common.graphtraversal import bfs

input = open('day20.txt').read().splitlines()

Coords = tuple[int, int]

def getPortal(grid: ArrayGrid, x: int, y: int) -> Optional[tuple[str, Coords]]:
  v = grid.getValue(x, y)
  if not v.isupper():
    return None

  # How to find the portal position.
  checks = {
    (1, 0): [(-1, 0),(2, 0)],
    (0, 1): [(0, -1),(0, 2)],
  }
  for dx, dy in checks:
    vd = grid.getValue(x + dx, y + dy, ' ')
    if vd.isupper():
      for cx, cy in checks[(dx, dy)]:
        nx, ny = x + cx, y + cy
        if grid.getValue(nx,ny,' ') == '.':
          return (v + vd, (nx, ny))
  return None

def getAdjacentNodes(
  grid: ArrayGrid,
  portals: dict[Coords, Coords],
  pos: Coords,
) -> list[tuple[Coords, Any]]:
  x, y = pos
  results = []
  for nx, ny in grid.getAdjacentCoords(x, y):
    v = grid.getValue(nx, ny)
    if v == '.':
      # Regular traversal.
      results.append(((nx, ny), None))
    elif v.isupper() and pos in portals:
      # Portal.
      results.append((portals[pos], None))
  return results

def part1() -> None:
  w = len(input[2]) + 2
  h = len(input)
  print('size: %d x %d' % (w, h))

  grid = ArrayGrid(w, h)
  for y in range(h):
    for x in range(w):
      v = input[y][x] if x < len(input[y]) else ' '
      grid.setValue(x, y, v)
  grid.print2D()

  start, end = None, None
  portalCoords = defaultdict(list)
  for y in range(h):
    for x in range(w):
      v = grid.getValue(x, y)
      portal = getPortal(grid, x, y)
      if portal is None:
        continue

      label, pos = portal
      if label == 'AA':
        assert start is None, 'already found start'
        start = pos
      elif label == 'ZZ':
        assert end is None, 'already found end'
        end = pos
      else:
        portalCoords[label].append(pos)

  assert start is not None, 'did not find start'
  assert end is not None, 'did not find end'
  print('start / end:', start, end)
  print('portals:', portalCoords)

  portals = {}
  for v1, v2 in portalCoords.values():
    portals[v1] = v2
    portals[v2] = v1
  print('links:', portals)

  result = bfs(
    start,
    lambda pos: getAdjacentNodes(grid, portals, pos),
    lambda x, y: True,
  )
  print(result[end])

part1()
