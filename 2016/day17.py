from typing import Iterable
from common.shortestpath import dijkstra
from common.arraygrid import ArrayGrid
from common.md5 import md5hash

input = open('day17.txt').read().rstrip()

Coords = tuple[int, int]
Node = tuple[Coords, str] # (position, path)

def hash(s: str) -> str:
  hi = '%s%s' %(input, s)
  return md5hash(hi)

def initGrid(w: int, h: int) -> ArrayGrid:
  grid = ArrayGrid(w, h)
  for y in range(h):
    for x in range(w):
      v = ' '
      if y == 0 or x == 0:
        v = '#'
      elif y == h - 1:
        if x < w - 2:
          v = '#'
      elif x == w - 1:
        if y < h - 2:
          v = '#'
      elif y % 2 == 0:
        v = '#' if x % 2 == 0 else '-'
      elif x % 2 == 0:
        v = '|'
      grid.setValue(x, y, v)

  return grid

def isOpen(ch: str) -> bool:
  assert len(ch) == 1, 'bad char input'
  return ch in {'b', 'c', 'd', 'e', 'f'}

def getAdjacent(grid: ArrayGrid, node: Node) -> Iterable[tuple[Node, int]]:
  (x, y), path = node

  deltas = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
  }
  indexes = ['U', 'D', 'L', 'R']

  for deltaStr in deltas:
    dx, dy = deltas[deltaStr]
    nx, ny = x + dx, y + dy
    if not grid.areCoordsWithinBounds(nx, ny):
      continue
    v = grid.getValue(nx, ny)
    if v == '#':
      continue

    assert v in ['-', '|'], 'bad grid value'

    ch = hash(path)[indexes.index(deltaStr)]
    if not isOpen(ch):
      continue

    newPath = '%s%s' % (path, deltaStr)
    # Move one space past the door.
    yield ((nx + dx, ny + dy), newPath), 1

def findLongestPathLen(grid: ArrayGrid, startNode: Node, end: Coords) -> int:
  result = 0
  q: list[tuple[Node, int]] = [(startNode, 0)] # (node, number of steps)
  while len(q) > 0:
    node, pathlen = q.pop(0)

    if node[0] == end:
      result = max(result, pathlen)
      continue

    for adjNode, _ in getAdjacent(grid, node):
      q.append((adjNode, pathlen + 1))

  return result

def part1() -> None:
  w, h = 9, 9
  grid = initGrid(w, h)
  start = 1, 1
  end = w - 2, h - 2
  grid.print2D()

  r = dijkstra((start, ''), lambda n: getAdjacent(grid, n), lambda n: n[0] == end)
  assert r[0] is not None, 'dijkstra did not find result'
  print(r[0][1])

def part2() -> None:
  w, h = 9, 9
  grid = initGrid(w, h)
  start = 1, 1
  end = w - 2, h - 2
  grid.print2D()

  print(findLongestPathLen(grid, (start, ''), end))

part2()
