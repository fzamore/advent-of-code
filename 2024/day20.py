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

def getCheatEnds(grid: ArrayGrid, cheatStart: Coords, cheatLength: int) -> Iterable[Coords]:
  ends = set()
  def visit(pos: Coords, numSteps: int) -> bool:
    if numSteps > cheatLength:
      return False

    if pos != cheatStart:
      ends.add(pos)
    return True

  bfs(cheatStart, lambda p: grid.getAdjacentCoords(p[0], p[1]), visit)
  return ends

def tryCheats(
  grid: ArrayGrid,
  start: Coords,
  end: Coords,
  cheatLength: int = 2,
  threshold: int = 100,
) -> int:
  cheatsToTry = set()
  def getAdj(pos: Coords) -> Iterable[Coords]:
    x, y = pos
    for ax, ay, v in grid.getAdjacentItems(x, y):
      if v != '#':
        yield ax, ay
      else:
        if (x, y) not in cheatsToTry:
          # Always use the first value we encounter, as that is guaranteed
          # to be the lowest distance in BFS order.
          cheatsToTry.add((x, y))

  bfsResult = bfs(start, getAdj, isEndNode=lambda p: p == end)

  print('cheats to try:', len(cheatsToTry))
  assert end in bfsResult, 'did not find end'
  shortestPathLength = bfsResult[end]
  print('shortest path length:', shortestPathLength)
  print()

  cheats = {}
  for cheatStart in cheatsToTry:
    c1x, c1y = cheatStart
    assert grid.getValue(c1x, c1y) != '#', 'all c1 should be open'
    for cheatEnd in getCheatEnds(grid, cheatStart, cheatLength):
      c2x, c2y = cheatEnd
      if grid.getValue(c2x, c2y, '#') == '#':
        # The cheat would not land back on the track. Skip.
        continue

      if cheatEnd not in bfsResult:
        # If the cheat doesn't get us back on the shortest path, then skip.
        continue

      # The length of the new path is the sum of a/ the distance the cheat
      # start, b/ manhattan distance betwen cheat start and cheat end, and
      # c/ the distance from cheat end to the course end.
      cheatDist = abs(c1x - c2x) + abs(c1y - c2y)
      assert cheatDist <= cheatLength, 'cheat was too long: %s %s %d' % (cheatStart, cheatEnd, cheatDist)
      pathLength = bfsResult[cheatStart] + cheatDist + (shortestPathLength - bfsResult[cheatEnd])
      if pathLength >= shortestPathLength:
        # There is no savings on this path. Skip.
        continue

      savings = shortestPathLength - pathLength
      assert savings > 0, 'should have already checked for savings.'

      assert (cheatStart, cheatEnd) not in cheats, 'already seen cheat'
      cheats[cheatStart, cheatEnd] = savings


  # Useful for debugging.
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

def part2() -> None:
  grid, start, end = parseInput()
  print('start/end:', start, end)

  print(tryCheats(grid, start, end, 20))

part2()
