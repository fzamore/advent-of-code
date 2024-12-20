from collections import Counter
from typing import Iterable
from common.graphtraversal import bfs
from common.arraygrid import ArrayGrid

input = open('day20.txt').read().splitlines()

Coords = tuple[int, int]
Delta = tuple[int, int]

def parseInput() -> tuple[ArrayGrid, Coords, Coords]:
  grid = ArrayGrid.gridFromInput(input)
  start, end = None, None
  for x, y, v in grid.getItems():
    if v == 'S':
      start = x, y
    if v == 'E':
      end = x, y
  assert start is not None and end is not None, 'did not find start/end'
  return grid, start, end

def tryCheats(grid: ArrayGrid, start: Coords, end: Coords, threshold: int = 100) -> int:
  # Map of cheat coordinate to try (must be a wall) to the node that led us there.
  cheatsToTry = {}
  def getAdj(pos: Coords) -> Iterable[Coords]:
    x, y = pos
    for ax, ay, v in grid.getAdjacentItems(x, y):
      if v != '#':
        yield ax, ay
      else:
        if (ax, ay) not in cheatsToTry:
          # Always use the first value we encounter, as that is guaranteed
          # to be the lowest in BFS order.
          cheatsToTry[ax, ay] = pos

  bfsResult = bfs(start, getAdj, isEndNode=lambda p: p == end)

  print('cheats to try:', len(cheatsToTry))
  assert end in bfsResult, 'did not find end'
  shortestPathLength = bfsResult[end]
  print('shortest path length:', shortestPathLength)
  print()

  cheats = {}
  for c1 in cheatsToTry:
    c1x, c1y = c1
    assert grid.getValue(c1x, c1y) == '#', 'all c1 should be walls: %s' % str(c1)
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
      c2x, c2y = c1x + dx, c1y + dy
      c2 = c2x, c2y
      if grid.getValue(c2x, c2y, '#') == '#':
        # The cheat would not land back on the track. Skip.
        continue

      if c2 not in bfsResult:
        # If the cheat doesn't get us back on the shortest path, then skip.
        continue

      prevNode = cheatsToTry[c1]

      # The length of the new path is the sum of a/ the distance to the
      # previous node, b/ 2 (for c1 & c2), and c/ the distance from c2 to
      # the end.
      pathLength = bfsResult[prevNode] + 2 + (shortestPathLength - bfsResult[c2])
      if pathLength >= shortestPathLength:
        # There is no savings on this path. Skip.
        continue

      savings = shortestPathLength - pathLength
      assert savings > 0, 'should have already checked for savings.'

      assert (c1, c2) not in cheats, 'already seen cheat'
      cheats[c1, c2] = savings


  # # Useful for debugging.
  # cheatsBySavings: dict[int, int] = Counter()
  # for c1, c2 in cheats:
  #   cheatsBySavings[cheats[c1, c2]] += 1
  # for k in sorted(cheatsBySavings.keys()):
  #   print('savings count:', cheatsBySavings[k], k)

  return sum([1 for c in cheats if cheats[c] >= threshold])

def part1() -> None:
  grid, start, end = parseInput()
  print('start/end:', start, end)

  print(tryCheats(grid, start, end))

part1()
