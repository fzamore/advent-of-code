from typing import Iterable
from common.shortestpath import dijkstra
from common.graphtraversal import bfs

input = int(open('day13.txt').read().rstrip())

Coords = tuple[int, int]

def isOpen(x: int, y: int) -> bool:
  if x < 0 or y < 0:
    return False
  t = x * x + 3 * x + 2 * x * y + y + y * y + input
  return bin(t)[2:].count('1') % 2 == 0

def getAdj(pos: Coords) -> Iterable[Coords]:
  x, y = pos
  deltas = [(0, 1), (0, -1), (1, 0),(-1, 0)]
  for dx, dy in deltas:
    nx, ny = x + dx, y + dy
    if isOpen(nx, ny):
      yield nx, ny

def getAdjDijkstra(pos: Coords) -> Iterable[tuple[Coords, int]]:
  for np in getAdj(pos):
    yield np, 1

def part1() -> None:
  start = 1, 1
  end = 31, 39

  r = dijkstra(start, getAdjDijkstra, lambda p: p == end)
  print(r[1])

def part2() -> None:
  start = 1, 1

  seen = set()
  def visit(pos, steps):
    assert pos not in seen, 'already visited coords'
    if steps > 50:
      return False
    seen.add(pos)
    return True

  bfs(start, getAdj, visit)
  print(len(seen))

part2()
