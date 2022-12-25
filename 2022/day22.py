from collections import namedtuple
from typing import Callable
from common.sparsegrid import SparseGrid

input = open('day22.txt').read()
IS_SAMPLE = False

Heading = tuple[int, int]
Position = tuple[int, int]

CubeFace = namedtuple('CubeFace', [
  'id', # int [0-5]
  'adjNorth', # (id, incomingEdge, isReversed)
  'adjEast', # (id, incomingEdge, isReversed)
  'adjSouth', # (id, incomingEdge, isReversed)
  'adjWest', # (id, incomingEdge, isReversed)
])

SAMPLE_CUBE_SIZE = 4
REAL_CUBE_SIZE = 50

def createGrid() -> SparseGrid:
  gridStr = input.split("\n\n")[0]

  grid = SparseGrid(2)
  y = 0
  for line in gridStr.splitlines():
    for x in range(len(line)):
      c = line[x]
      if c != ' ':
        grid.setValue((x, y), c)
    y += 1
  return grid

def initCubeFaces() -> dict[int, CubeFace]:
  if IS_SAMPLE:
    return {
      0: CubeFace(0, (1, 'N', 1), (5, 'E', 1), (3, 'N', 0), (2, 'N', 0)),
      1: CubeFace(1, (0, 'N', 1), (2, 'W', 0), (4, 'S', 1), (5, 'S', 0)),
      2: CubeFace(2, (0, 'W', 0), (3, 'W', 0), (4, 'W', 1), (1, 'E', 0)),
      3: CubeFace(3, (0, 'S', 0), (5, 'N', 1), (4, 'N', 0), (2, 'E', 0)),
      4: CubeFace(4, (3, 'S', 0), (5, 'W', 0), (1, 'S', 1), (2, 'S', 1)),
      5: CubeFace(5, (3, 'E', 1), (0, 'E', 1), (1, 'W', 1), (4, 'E', 0)),
    }
  else:
    return {
      0: CubeFace(0, (5, 'W', 0), (1, 'W', 0), (2, 'N', 0), (3, 'W', 1)),
      1: CubeFace(1, (5, 'S', 0), (4, 'E', 1), (2, 'E', 0), (0, 'E', 0)),
      2: CubeFace(2, (0, 'S', 0), (1, 'S', 0), (4, 'N', 0), (3, 'N', 0)),
      3: CubeFace(3, (2, 'W', 0), (4, 'W', 0), (5, 'N', 0), (0, 'W', 1)),
      4: CubeFace(4, (2, 'S', 0), (1, 'E', 1), (5, 'E', 0), (3, 'E', 0)),
      5: CubeFace(5, (3, 'S', 0), (4, 'S', 0), (1, 'N', 0), (0, 'N', 0)),
    }

def initCubeFacePositions() -> dict[Position, int]:
  if IS_SAMPLE:
    return {
      (2, 0): 0,
      (0, 1): 1,
      (1, 1): 2,
      (2, 1): 3,
      (2, 2): 4,
      (3, 2): 5,
    }
  else:
    return {
      (1, 0): 0,
      (2, 0): 1,
      (1, 1): 2,
      (0, 2): 3,
      (1, 2): 4,
      (0, 3): 5,
    }

def getPathInstructions() -> list[int | str]:
  pathStr = input.split("\n\n")[1]
  pathStr = pathStr.splitlines()[0]
  result: list[int | str] = []
  i = 0
  startNum = 0
  while i < len(pathStr):
    c = pathStr[i]
    if c in ['L', 'R']:
      numSpaces = int(pathStr[startNum:i])
      startNum = i + 1
      result.append(numSpaces)
      result.append(c)
    i += 1
  result.append(int(pathStr[startNum:i]))
  return result

def rotate(heading: Heading, dir: str) -> Heading:
  assert dir in ['L', 'R']
  match heading:
    case (1, 0):
      return (0, -1) if dir == 'L' else (0, 1)
    case (-1, 0):
      return (0, 1) if dir == 'L' else (0, -1)
    case (0, 1):
      return (1, 0) if dir == 'L' else (-1, 0)
    case (0, -1):
      return (-1, 0) if dir == 'L' else (1, 0)
    case _:
      assert False, 'bad heading'

def getNextPositionAndHeading(
  grid: SparseGrid,
  pos: Position,
  heading: Heading,
  rowBounds: tuple[int, int],
  colBounds: tuple[int, int],
) -> tuple[Position, Heading]:
  x, y = pos
  assert grid.getValue((x, y)) == '.', 'pos in bad spot: (%d, %d)' %(x, y)
  dx, dy = heading
  cmin, cmax = rowBounds
  rmin, rmax = colBounds
  mx, my = x - cmin, y - rmin
  colMod = cmax - cmin + 1
  rowMod = rmax - rmin + 1

  tx, ty = ((mx + dx) % colMod, (my + dy) % rowMod)
  mx, my = tx, ty

  result = (mx + cmin, my + rmin)
  assert grid.hasValue(result), \
    'result in bad spot: (%d, %d)' % (result[0], result[1])
  return (result, heading)

def getCubeFaceIDForPosition(
  grid: SparseGrid,
  cubeFacePositions: dict[Position, int],
  cubeSize: int,
  pos: Position,
) -> int:
  x, y = pos
  if not grid.hasValue((x, y)):
    return -1
  return cubeFacePositions[(x // cubeSize, y // cubeSize)]

def getNextPositionAndHeading2(
  grid: SparseGrid,
  pos: Position,
  heading: Heading,
  cubeFaces: dict[int, CubeFace],
  cubeFacePositions: dict[Position, int],
  cubeSize: int,
) -> tuple[Position, Heading]:
  x, y = pos
  assert grid.getValue(pos) == '.', 'pos is not an empty grid spot: (%d, %d)' % (x, y)
  cubeFaceID = getCubeFaceIDForPosition(grid, cubeFacePositions, cubeSize, pos)
  assert 0 <= cubeFaceID <= 5, 'bad cubeface for position: (%d, %d)' % (x, y)
  dx, dy = heading
  npos = x + dx, y + dy
  nCubeFaceID = getCubeFaceIDForPosition(grid, cubeFacePositions, cubeSize, npos)
  if cubeFaceID == nCubeFaceID:
    # We're still on the same cube face, so we don't need fancy calculations.
    return npos, heading

  cubeFace = cubeFaces[cubeFaceID]
  match heading:
    case (1, 0):
      outgoingEdge = 'E'
      nCubeFaceID, incomingEdge, isReversed = cubeFace.adjEast
    case (-1, 0):
      outgoingEdge = 'W'
      nCubeFaceID, incomingEdge, isReversed = cubeFace.adjWest
    case (0, 1):
      outgoingEdge = 'S'
      nCubeFaceID, incomingEdge, isReversed = cubeFace.adjSouth
    case (0, -1):
      outgoingEdge = 'N'
      nCubeFaceID, incomingEdge, isReversed = cubeFace.adjNorth
    case _:
      assert False, 'bad heading in getNextPositionAndHeading2'

  mx, my = x % cubeSize, y % cubeSize
  reverseCubeFacePositions = {v: k for k, v in cubeFacePositions.items()}
  nCubeFaceX, nCubeFaceY = reverseCubeFacePositions[nCubeFaceID]

  # Calculate the new "variable" coordinate along the incoming edge (e.g.,
  # if incoming edge is N, then calculate the x coordinate).
  match incomingEdge:
    case 'N' | 'S':
      match outgoingEdge:
        case 'S' | 'N':
          nmx = mx if not isReversed else (cubeSize - 1) - mx
        case 'E' | 'W':
          nmx = my if not isReversed else (cubeSize - 1) - my
      nx = nmx + cubeSize * nCubeFaceX

    case 'E' | 'W':
      match outgoingEdge:
        case 'S' | 'N':
          nmy = mx if not isReversed else (cubeSize - 1) - mx
        case 'E' | 'W':
          nmy = my if not isReversed else (cubeSize - 1) - my
      ny = nmy + cubeSize * nCubeFaceY

    case _: assert False, 'bad incoming edge'

  # Calculate the new heading and new "fixed" coordinate, which will
  # always be either a multiple of the cube size or a multiple of the cube
  # size minus 1 (e.g., if incoming edge is N, then calculate the y
  # coordinate).
  match incomingEdge:
    case 'N':
      nHeading = (0, 1)
      ny = cubeSize * nCubeFaceY
    case 'E':
      nHeading = (-1, 0)
      nx = cubeSize * (nCubeFaceX + 1) - 1
    case 'S':
      nHeading = (0, -1)
      ny = cubeSize * (nCubeFaceY + 1) - 1
    case 'W':
      nHeading = (1, 0)
      nx = cubeSize * nCubeFaceX
    case _: assert False, 'bad incoming edge'

  assert grid.hasValue((nx, ny)), 'new value not in grid: (%d, %d)' % (nx, ny)
  return (nx, ny), nHeading

def moveForward(
  grid: SparseGrid,
  pos: Position,
  heading: Heading,
  getNextFn: Callable[[SparseGrid, Position, Heading], tuple[Position, Heading]],
  numSpaces: int,
) -> tuple[Position, Heading]:
  x, y = pos
  assert grid.getValue((x, y)) == '.', 'pos in bad spot: (%d, %d)' %(x, y)
  for _ in range(numSpaces):
    npos, nheading = getNextFn(grid, pos, heading)
    if grid.getValue(npos) == '#':
      break
    pos = npos
    heading = nheading

  x, y = pos
  assert grid.getValue(pos) == '.', 'result in bad spot: (%d, %d)' % (x, y)
  return pos, heading

def part1():
  grid = createGrid()

  maxX, maxY = grid.getMaxCoords()

  rowBounds = []
  for y in range(maxY + 1):
    x = 0
    while not grid.hasValue((x, y)):
      x += 1
    rowMin = x
    while grid.hasValue((x, y)) and x <= maxX:
      x += 1
    rowMax = x - 1
    rowBounds.append((rowMin, rowMax))

  colBounds = []
  for x in range(maxX + 1):
    y = 0
    while not grid.hasValue((x, y)):
      y += 1
    colMin = y
    while grid.hasValue((x, y)) and y <= maxY:
      y += 1
    colMax = y - 1
    colBounds.append((colMin, colMax))

  assert len(rowBounds) == maxY + 1
  assert len(colBounds) == maxX + 1

  pos = (rowBounds[0][0], 0)
  heading = (1, 0)
  print('starting pos:', pos)

  for instr in getPathInstructions():
    if instr in ['L', 'R']:
      heading = rotate(heading, instr)
    else:
      def getNextFn(
        grid: SparseGrid,
        pos: Position,
        heading: heading,
      ) -> tuple[Position, Heading]:
        return getNextPositionAndHeading(
          grid,
          pos,
          heading,
          rowBounds[pos[1]],
          colBounds[pos[0]],
        )
      numSpaces = int(instr)
      pos, _ = moveForward(grid, pos, heading, getNextFn, numSpaces)

  print('final pos:', pos)
  print('final heading', heading)
  headingScore = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3,
  }[heading]
  x, y = pos
  print(4 * (x + 1) + 1000 * (y + 1) + headingScore)

def part2():
  if IS_SAMPLE:
    cubeSize = SAMPLE_CUBE_SIZE
  else:
    cubeSize = REAL_CUBE_SIZE

  grid = createGrid()
  cubeFaces = initCubeFaces()
  cubeFacePositions = initCubeFacePositions()

  print('cube size:', cubeSize)

  startX = input.splitlines()[0].index('.')
  assert startX % cubeSize == 0, 'bad startX: %d' % startX
  pos = (startX, 0)
  heading = (1, 0)
  print('starting pos:', pos)

  for instr in getPathInstructions():
    if instr in ['L', 'R']:
      heading = rotate(heading, instr)
      print('after rotation', instr, heading)
    else:
      def getNextFn(
        grid: SparseGrid,
        pos: Position,
        heading: heading,
      ) -> tuple[Position, Heading]:
        return getNextPositionAndHeading2(
          grid,
          pos,
          heading,
          cubeFaces,
          cubeFacePositions,
          cubeSize,
        )
      numSpaces = int(instr)
      pos, nHeading = moveForward(grid, pos, heading, getNextFn, numSpaces)
      heading = nHeading
      print('after moving', numSpaces, pos, heading)

  print('final pos:', pos)
  print('final heading', heading)
  headingScore = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3,
  }[heading]
  x, y = pos
  print(4 * (x + 1) + 1000 * (y + 1) + headingScore)

part2()
