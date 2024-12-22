from typing import Iterable
from common.arraygrid import ArrayGrid
from common.shortestpath import dijkstraAllShortestPaths

input = open('day21.txt').read().splitlines()

Coords = tuple[int, int]
Delta = tuple[int, int]
DeltaPath = Iterable[Delta]
StrPath = list[str]
Seq = str

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

# Takes a list of all paths between adjacent nodes, and explodes it into a
# single list of paths.
def consolidatePaths(allSeqPaths: list[list[StrPath]], seqi: int = 0) -> list[StrPath]:
  if seqi == len(allSeqPaths):
    return [[]]

  result = []
  for prefix in allSeqPaths[seqi]:
    for suffix in consolidatePaths(allSeqPaths, seqi + 1):
      result.append(prefix + suffix)
  return result

# Finds all paths for the given sequence from the given start in the given
# grid.
def findAllPathsForSeq(grid: ArrayGrid, gridStart: Coords, seq: Seq) -> list[StrPath]:
  allSeqPaths = []
  start = gridStart
  reverseMap = convertGridToReverseMap(grid)

  # Go through the sequence.
  for c in seq:
    target = reverseMap[c]
    # Find all paths from start to that character.
    deltaPaths = findAllDeltaPathsBetweenCells(grid, start, target)

    # Reset the start for the next iteration.
    start = target

    # Add all start -> target paths to the list of paths for the entire
    # sequence.
    allNodePaths = []
    for deltaPath in deltaPaths:
      # Add the button press to the path.
      strPath = convertDeltaPathToStrPath(deltaPath) + ['A']
      allNodePaths.append(strPath)
    allSeqPaths.append(allNodePaths)

  return consolidatePaths(allSeqPaths)

# Finds all shortest paths for the given sequence in the given grid.
def getShortestPathsForSeq(grid: ArrayGrid, start: Coords, seq: Seq) -> list[StrPath]:
  paths = findAllPathsForSeq(grid, start, seq)
  pathlen = min([len(p) for p in paths])
  return [p for p in paths if len(p) == pathlen]

# Find the best path length for the given sequence, in the given list of
# grids and start positions (the first grid is the numeric grid).
def findBestSeqPerLevel(
  grids: tuple[ArrayGrid, ArrayGrid],
  levels: int,
  starts: list[Coords],
  inputSeq: Seq,
) -> dict[int, Seq]:
  assert levels == len(starts), 'bad input to bestLengthForSeq'
  bestSeqForLevel: dict[int, Seq] = {}

  numericGrid, directionalGrid = grids

  seqs = [(0, inputSeq)]
  while len(seqs) > 0:
    level, seq = seqs.pop(0)
    if level == levels:
      # We've reached the last level. Stop.
      continue

    # The first level is the numeric grid, and all other levels are the
    # directional grid.
    grid = numericGrid if level == 0 else directionalGrid
    start = starts[level]

    paths = getShortestPathsForSeq(grid, start, seq)
    for path in paths:
      pathseq = ''.join(path)
      bestSeq = bestSeqForLevel.get(level)
      if bestSeq is None or len(pathseq) <= len(bestSeq):
        # We've found a sequence at least as good for this level.
        bestSeqForLevel[level] = pathseq
        seqs.append((level + 1, pathseq))

  return bestSeqForLevel

def part1() -> None:
  numericGrid, numericStart = initNumericGrid()
  print('nstart:', numericStart)
  numericGrid.print2D({None: '.'})

  directionalGrid, directionalStart = initDirectionalGrid()
  print('dstart:', directionalStart)
  directionalGrid.print2D({None: '.'})

  levels = 3

  rnmap = convertGridToReverseMap(numericGrid)
  rdmap = convertGridToReverseMap(directionalGrid)

  ans = 0
  for seq in input:
    grids = [numericGrid]
    starts = [numericStart]
    for _ in range(levels - 1):
      grids.append(directionalGrid)
      starts.append(directionalStart)

    # Split the sequence up into characters, since it's far cheaper to
    # compute the sequence for each individual character.
    bestLength = 0
    for c in seq:
      bestSeqPerLevel = findBestSeqPerLevel((numericGrid, directionalGrid), levels, starts, c)
      print('bestSeqPerLevel:', c, bestSeqPerLevel)

      # Add the length of the sequence of the last level to our total.
      bestLength += len(bestSeqPerLevel[levels - 1])

      # Compute the new starting positions for each level.
      newStarts = [rnmap[c]]
      for level in range(levels - 1):
        newStarts.append(rdmap[bestSeqPerLevel[level][-1]])
      starts = newStarts
      print('seq result:', seq, bestLength)

    ans += bestLength * int(seq[:-1])

  print(ans)

part1()
