from functools import cache
from typing import Iterable
from common.arraygrid import ArrayGrid
from common.shortestpath import dijkstraAllShortestPaths

input = open('day21.txt').read().splitlines()

Coords = tuple[int, int]
Delta = tuple[int, int]
DeltaPath = Iterable[Delta]
StrPath = list[str]

def initNumericGrid() -> tuple[ArrayGrid, Coords]:
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

  grid = ArrayGrid(3,4)
  for (x, y), v in data:
    grid.setValue(x, y, str(v))
  return grid, (2, 3)

def initDirectionalGrid() -> tuple[ArrayGrid, Coords]:
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
  return grid, (2, 0)

def convertGridToReverseMap(grid: ArrayGrid) -> dict[str, Coords]:
  r = {}
  for x, y, v in grid.getItems():
    if v is not None:
      r[str(v)] = x, y
  return r

# Converts the given past as a list of coords to a list of deltas.
def convertPathToDeltas(coordsPath: list[Coords]) -> DeltaPath:
  for i in range(len(coordsPath) - 1):
    x, y = coordsPath[i]
    nx, ny = coordsPath[i + 1]
    dx, dy = nx - x, ny - y
    yield dx, dy

# Finds all shortest paths between the two given cells in the given grid.
# Each path in the return value is expressed as a list of (dx, dy) deltas
# between adjacent nodes in the path.
def findAllDeltaPathsBetweenCells(grid: ArrayGrid, start: Coords, end: Coords) -> Iterable[DeltaPath]:
  def getAdj(pos: Coords) -> Iterable[tuple[Coords, int]]:
    x, y = pos
    for ax, ay in grid.getAdjacentCoords(x, y):
      if grid.hasValue(ax, ay):
        yield (ax, ay), 1

  r = dijkstraAllShortestPaths(start, getAdj, lambda p: p == end)
  for path in r[2]:
    yield convertPathToDeltas(path)

def convertDeltaPathToStrPath(deltaPath: Iterable[Delta]) -> StrPath:
  deltaMap = {
    (1, 0): '>',
    (0, 1): 'v',
    (-1, 0): '<',
    (0, -1): '^',
  }
  return [deltaMap[d] for d in deltaPath]

# Finds all paths from start to the given character in the given grid.
def findAllShortestPathsToChar(grid: ArrayGrid, start: Coords, char: str) -> Iterable[StrPath]:
  assert len(char) == 1, 'sequence must be of length 1'
  reverseMap = convertGridToReverseMap(grid)

  target = reverseMap[char]
  # Find all paths from start to that character.
  for deltaPath in findAllDeltaPathsBetweenCells(grid, start, target):
    # Add the button press to the path.
    yield convertDeltaPathToStrPath(deltaPath) + ['A']

def solve(levels: int) -> int:
  numericGrid, numericStart = initNumericGrid()
  print('nstart:', numericStart)
  numericGrid.print2D({None: '.'})

  directionalGrid, directionalStart = initDirectionalGrid()
  print('dstart:', directionalStart)
  directionalGrid.print2D({None: '.'})

  rnmap = convertGridToReverseMap(numericGrid)
  rdmap = convertGridToReverseMap(directionalGrid)

  # Advances the sequence by a the given single character in the given
  # grid at the given recursive level. Returns the number of characters
  # ultimately needed to express that character.
  @cache
  def advanceByOneChar(grid: ArrayGrid, start: Coords, level: int, char: str) -> int:
    assert len(char) == 1, 'bad char'

    if level == 0:
      assert grid == directionalGrid, 'bad grid'
      paths = findAllShortestPathsToChar(grid, start, char)
      for path in paths:
        return len(path)
      assert False, 'should have found a path'

    bestNumChars = float('inf')
    paths = findAllShortestPathsToChar(grid, start, char)
    for path in paths:
      numChars = 0
      dstart = directionalStart
      for pathchar in path:
        numChars += advanceByOneChar(directionalGrid, dstart, level - 1, pathchar)
        # Update the start position for the next char in the sequence.
        dstart = rdmap[pathchar]

      # Keep track of our best result so far.
      bestNumChars = min(numChars, bestNumChars)

    return int(bestNumChars)

  result = 0
  for seq in input:
    seqLength = 0
    start = numericStart
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
