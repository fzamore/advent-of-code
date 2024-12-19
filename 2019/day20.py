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

def processInput(w: int, h: int) \
  -> tuple[ArrayGrid, dict[Coords, Coords], Coords, Coords]:
  grid = ArrayGrid(w, h)
  for y in range(h):
    for x in range(w):
      v = input[y][x] if x < len(input[y]) else ' '
      grid.setValue(x, y, v)

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
        print('portal', label, pos)
        portalCoords[label].append(pos)

  assert start is not None, 'did not find start'
  assert end is not None, 'did not find end'

  portals = {}
  for v1, v2 in portalCoords.values():
    portals[v1] = v2
    portals[v2] = v1

  return grid, portals, start, end

def getAdjacentNodes(
  grid: ArrayGrid,
  portals: dict[Coords, Coords],
  pos: Coords,
) -> list[Coords]:
  x, y = pos
  results = []
  for nx, ny in grid.getAdjacentCoords(x, y):
    v = grid.getValue(nx, ny)
    if v == '.':
      # Regular traversal.
      results.append((nx, ny))
    elif v.isupper() and pos in portals:
      # Portal.
      results.append(portals[pos])
  return results

def isOuterPortal(grid: ArrayGrid, pos: Coords) -> bool:
  w, h = grid.getWidth(), grid.getHeight()
  x, y = pos
  # Crude method to determine whether the given position is within N
  # points of the border, and if so, it's an outer portal.
  return any([v <= 5 for v in [x, abs(x - w), y, abs(y - h)]])

def getAdjacentNodes2(
  grid: ArrayGrid,
  portals: dict[Coords, Coords],
  node: tuple[Coords, int],
) -> list[tuple[Coords, int]]:
  pos, level = node
  x, y = pos
  results = []
  for nx, ny in grid.getAdjacentCoords(x, y):
    v = grid.getValue(nx, ny)
    if v == '.':
      # Regular traversal.
      results.append(((nx, ny), level))
    elif v.isupper() and pos in portals:
      # An uppercase letter is adjacent to (x, y), so (x, y) must be a portal.
      other = portals[pos]
      if isOuterPortal(grid, pos):
        assert not isOuterPortal(grid, other), 'other end should not also be outer'
        if level == 1:
          # We can't pass through an outer portal if we're at the top level.
          continue
        # Move outward.
        nlevel = level - 1
      else:
        assert isOuterPortal(grid, other), 'other end should be outer'
        # Move inward.
        nlevel = level + 1
      results.append((other, nlevel))
  return results

def part1() -> None:
  w = len(input[2]) + 2
  h = len(input)
  print('size: %d x %d' % (w, h))

  grid, portals, start, end = processInput(w, h)

  grid.print2D()
  assert start is not None, 'did not find start'
  assert end is not None, 'did not find end'
  print('start / end:', start, end)
  print('portals:', portals)

  result = bfs(start, lambda pos: getAdjacentNodes(grid, portals, pos))
  print(result[end])

def part2() -> None:
  w = len(input[2]) + 2
  h = len(input)
  print('size: %d x %d' % (w, h))

  grid, portals, start, end = processInput(w, h)

  grid.print2D()
  assert start is not None, 'did not find start'
  assert end is not None, 'did not find end'
  print('start / end:', start, end)
  print('portals:', portals)

  result = bfs(
    (start, 1),
    lambda node: getAdjacentNodes2(grid, portals, node),
    isEndNode=lambda node: node[0] == end and node[1] == 1,
  )
  print(result[(end, 1)])

part2()
