from collections import deque
from typing import Iterable

from common.shortestpath import dijkstraAllNodes
from common.sparsegrid import SparseGrid

input = open('day20.txt').read()[1:-2]

Coords = tuple[int, int]

# Given the start of a group (branch), return the start index for each
# option.
def getGroupStarts(S: str, i: int) -> list[int]:
  assert S[i] == '(', 'bad group start'
  i += 1
  result = [i]
  c = 1
  while c > 0:
    v = S[i]
    if v == '(':
      c += 1
    elif v == ')':
      c -= 1
    elif v == '|' and c == 1:
      result.append(i + 1)
    i += 1
  return result

# Given the end of a group branch (i.e., a "|" character), return the end
# index of the corresponding group.
def getGroupEnd(S: str, i: int) -> int:
  assert S[i] == '|', 'bad group end'
  c = 1
  while c > 0:
    v = S[i]
    if v == '(':
      c += 1
    elif v == ')':
      c -= 1
    i += 1
  return i

def isChar(c: str) -> bool:
  return c in ['N', 'E', 'S', 'W']

# Given a starting index (which must be a non-symbol character), return
# the indicies for the next non-symbol character.
def getNextIndex(S: str, start: int) -> list[int]:
  assert isChar(S[start]), 'bad get next index input'
  result = []
  q = deque([start + 1])
  while len(q) > 0:
    i = q.popleft()

    if i >= len(S):
      # We've reached the end of the string.
      continue

    v = S[i]
    if isChar(v):
      result.append(i)
    elif v == '(':
      q.extend(getGroupStarts(S, i))
    elif v == '|':
      q.append(getGroupEnd(S, i))
    elif v == ')':
      q.append(i + 1)
    else:
      assert False, 'bad char'

  assert all([isChar(S[x]) for x in result]), 'bad result in getNextIndex'
  return result

def generateFullMap(S: str) -> SparseGrid:
  grid = SparseGrid(2)
  deltas = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
  }

  q = deque([((0, 0), 0)])
  seen = set()
  while len(q) > 0:
    (x, y), i = q.popleft()

    if i in seen:
      # Do not re-generate the map for indicies we've already seen. This
      # optimization is crucial. Without this, the algorithm won't
      # complete.
      continue
    seen.add(i)

    # Add the wall (i.e., door).
    dx, dy = deltas[S[i]]
    wx, wy = x + dx, y + dy
    wallchar = '|' if S[i] in ['E', 'W'] else '-'
    grid.setValue((wx, wy), wallchar)

    # Add the next room.
    nx, ny = wx + dx, wy + dy
    grid.setValue((nx, ny), '.')

    for ni in getNextIndex(S, i):
      q.append(((nx, ny), ni))

  grid.setValue((0, 0), 'X')
  return grid

def printGrid(grid: SparseGrid) -> None:
  minCoords, maxCoords = grid.getMinCoords(), grid.getMaxCoords()
  minCoords[0] -= 1
  minCoords[1] -= 1
  maxCoords[0] += 1
  maxCoords[1] += 1

  print()
  grid.print2D(default='#', minCoords=minCoords, maxCoords=maxCoords)
  print()

def computeAllDistances(grid: SparseGrid) -> dict[Coords, float]:
  def getAdj(pos: Coords) -> Iterable[tuple[Coords, int]]:
    x, y = pos
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in deltas:
      wx, wy = x + dx, y + dy
      v = grid.getValue((wx, wy), default='#')
      assert v != '.', 'invalid grid'
      if v in ['|', '-']:
        yield (wx + dx, wy + dy), 1

  return dijkstraAllNodes((0, 0), getAdj)

def part1() -> None:
  print('input:', len(input))
  print(input)
  assert isChar(input[0]), 'input must start with NESW'

  print()
  print('generating map...')
  grid = generateFullMap(input)
  print('done.')
  printGrid(grid)

  print()
  print('shortest path...')
  distances = computeAllDistances(grid)
  print('done.')

  maxCoords = max(distances, key=distances.__getitem__)
  print('max:', maxCoords, distances[maxCoords])
  print(distances[maxCoords])

def part2() -> None:
  print('input:', len(input))
  assert isChar(input[0]), 'input must start with NESW'

  print()
  print('generating map...')
  grid = generateFullMap(input)
  print('done.')

  distances = computeAllDistances(grid)

  print()
  print('number of rooms:', len(distances))
  print(len([k for k in distances if distances[k] >= 1000]))

part2()
