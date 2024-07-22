from typing import Iterable
from collections import deque

from common.shortestpath import dijkstraAllNodes
from common.sparsegrid import SparseGrid

input = open('day20.txt').read()[1:-2]

Coords = tuple[int, int]

def isChar(c: str) -> bool:
  return c in 'NESW'

def generateFullMap(S: str) -> SparseGrid:
  grid = SparseGrid(2)
  grid.setValue((0, 0), 'X')

  deltas = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
  }

  # I stole this approach from Reddit. It's an O(n) approach that goes
  # through the string a single time, maintaining current positions, group
  # starts, and group ends. It also maintains a stack to save state
  # whenever we begin and end a group.

  # We use sets to remove duplicates.
  curPositions = set([(0, 0)])
  groupStarts: set[Coords] = set()
  groupEnds: set[Coords] = set()
  stack: list[tuple[set[Coords], set[Coords]]] = []

  for ch in S:
    if isChar(ch):
      for x, y in curPositions.copy():
        # Process this position by removing it from the set.
        curPositions.remove((x, y))

        dx, dy = deltas[ch]

        # Add the wall (door) to the map only.
        wx, wy = x + dx, y + dy
        wallchar = '|' if ch in ['E', 'W'] else '-'
        grid.setValue((wx, wy), wallchar)

        # Add the next room.
        nx, ny = wx + dx, wy + dy
        grid.setValue((nx, ny), '.')
        curPositions.add((nx, ny))

    elif ch == '(':
      # Push our current group onto the stack and begin a new group.
      stack.append((groupStarts, groupEnds))
      groupStarts = curPositions.copy()
      groupEnds = set()

    elif ch == '|':
      # Add all current positions to our group ends.
      groupEnds.update(curPositions)
      curPositions = groupStarts.copy()

    elif ch == ')':
      groupStarts, groupEnds = stack.pop()

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
  print()
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
