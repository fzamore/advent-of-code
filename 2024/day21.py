from functools import cache
from typing import Iterable
from common.arraygrid import ArrayGrid
from common.shortestpath import dijkstraAllShortestPaths

input = open('day21.txt').read().splitlines()

Coords = tuple[int, int]
CharPath = list[str]

def initNumericGrid() -> ArrayGrid:
  data = (
    ((0, 0), 7),
    ((1, 0), 8),
    ((2, 0), 9),
    ((0, 1), 4),
    ((1, 1), 5),
    ((2, 1), 6),
    ((0, 2), 1),
    ((1, 2), 2),
    ((2, 2), 3),
    ((1, 3), 0),
    ((2, 3), 'A'),
  )
  grid = ArrayGrid(3, 4)
  for (x, y), v in data:
    grid.setValue(x, y, str(v))
  return grid

def initDirectionalGrid() -> ArrayGrid:
  data = (
    ((1, 0), '^'),
    ((2, 0), 'A'),
    ((0, 1), '<'),
    ((1, 1), 'v'),
    ((2, 1), '>'),
  )
  grid = ArrayGrid(3, 2)
  for (x, y), v in data:
    grid.setValue(x, y, v)
  return grid

def convertGridToReverseMap(grid: ArrayGrid) -> dict[str, Coords]:
  r = {}
  for x, y, v in grid.getItems():
    if v is not None:
      r[str(v)] = x, y
  return r

# Converts the given path as a list of coords to a list of characters representing deltas.
def convertCoordsPathToCharPath(coordsPath: list[Coords]) -> CharPath:
  deltaMap = {
    (1, 0): '>',
    (0, 1): 'v',
    (-1, 0): '<',
    (0, -1): '^',
  }

  strPath = []
  for i in range(len(coordsPath) - 1):
    x, y = coordsPath[i]
    nx, ny = coordsPath[i + 1]
    dx, dy = nx - x, ny - y
    strPath.append(deltaMap[(dx, dy)])
  return strPath

# Finds all shortest paths between the two given cells in the given grid.
# Each path in the return value is expressed as a list of directional
# characters (^, v, <, >,) between adjacent nodes in the path, plus the
# "A" button press at the end of each path.
def findAllShortestPathsBetweenCells(grid: ArrayGrid, start: Coords, end: Coords) -> Iterable[CharPath]:
  def getAdj(pos: Coords) -> Iterable[tuple[Coords, int]]:
    x, y = pos
    for ax, ay in grid.getAdjacentCoords(x, y):
      if grid.hasValue(ax, ay):
        yield (ax, ay), 1

  r = dijkstraAllShortestPaths(start, getAdj, lambda p: p == end)
  for path in r[2]:
    yield convertCoordsPathToCharPath(path) + ['A']

def solve(levels: int) -> int:
  numericGrid = initNumericGrid()
  numericGrid.print2D({None: '.'})

  directionalGrid = initDirectionalGrid()
  directionalGrid.print2D({None: '.'})

  rnmap = convertGridToReverseMap(numericGrid)
  rdmap = convertGridToReverseMap(directionalGrid)

  # Advances the sequence by a the given single character in the given
  # grid at the given recursive level. Returns the minimum number of
  # characters ultimately needed to express that character.
  @cache
  def advanceByOneChar(grid: ArrayGrid, start: Coords, level: int, char: str) -> int:
    assert len(char) == 1, 'bad char'

    # Find all shortest paths between start and destination for this particular grid.
    rmap = rnmap if grid == numericGrid else rdmap
    paths = findAllShortestPathsBetweenCells(grid, start, rmap[char])

    if level == 0:
      # Return the length of the first path, since all paths are equal lengths.
      return len(list(paths)[0])

    bestNumChars = float('inf')
    for path in paths:
      # Recursively calculate the total length of this path.
      numChars = 0
      dstart = rdmap['A']
      for pathchar in path:
        numChars += advanceByOneChar(directionalGrid, dstart, level - 1, pathchar)
        # Update the start position for the next char in the sequence.
        dstart = rdmap[pathchar]

      # Keep track of our best result so far.
      bestNumChars = min(numChars, bestNumChars)

    assert bestNumChars != float('inf'), 'did not find best path'
    return int(bestNumChars)

  result = 0
  for seq in input:
    seqLength = 0
    start = rnmap['A']
    for c in seq:
      seqLength += advanceByOneChar(numericGrid, start, levels, c)
      start = rnmap[c]
    print('seq:', seq, seqLength)
    result += seqLength * int(seq[:-1])
  return result

def part1() -> None:
  print(solve(2))

def part2() -> None:
  print(solve(25))

part2()
