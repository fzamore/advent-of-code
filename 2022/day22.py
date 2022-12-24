from typing import Callable
from common.sparsegrid import SparseGrid

input = open('day22.txt').read()

Heading = tuple[int, int]
Position = tuple[int, int]

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

def moveForward(
  grid: SparseGrid,
  pos: Position,
  heading: Heading,
  getNextFn: Callable[[SparseGrid, Position, Heading], tuple[Position, Heading]],
  numSpaces: int,
) -> Position:
  x, y = pos
  assert grid.getValue((x, y)) == '.', 'pos in bad spot: (%d, %d)' %(x, y)
  for _ in range(numSpaces):
    npos, _ = getNextFn(grid, pos, heading)
    if grid.getValue(npos) == '#':
      break
    pos = npos

  x, y = pos
  assert grid.getValue(pos) == '.', 'result in bad spot: (%d, %d)' % (x, y)
  return pos

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
      pos = moveForward(grid, pos, heading, getNextFn, numSpaces)

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

part1()
