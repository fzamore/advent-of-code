import sys
from typing import Iterator
from common.graphtraversal import dfs
from common.arraygrid import ArrayGrid
from enum import Enum, IntEnum

# This algorithm solves the "Battleship" puzles in Games Magazine by
# exhaustively trying every position for a battleship, then the two
# cruisers, etc. until all ships are placed. Input files are given as an
# 11x11 text file with the last row and the last column specifying the
# number of ships in that column or row. The rest of the characters are
# specified as follows:
#
#   .            Blank
#   |            Water
#   < > ^ v      End of ship
#   H            Middle of ship
#   O            Submarine
#
# For example:
#    .<........4
#    ..........0
#    ..........4
#    ..........2
#    ..........3
#    ....v.....1
#    ..........2
#    ..O.......2
#    ..........1
#    ..........1
#    2120613041

WATER= '|'
SIZE = 10

class Ship(IntEnum):
  SUBMARINE = 1
  DESTROYER = 2
  CRUISER = 3
  BATTLESHIP = 4

Coords = tuple[int, int]
Delta = tuple[int, int]
ShipsRemaining = tuple[tuple[Ship, int], tuple[Ship, int], tuple[Ship, int], tuple[Ship, int]]
DfsNode = tuple[ArrayGrid, ShipsRemaining]

class Orientation(Enum):
  HORIZONTAL = 1
  VERTICAL = 2

def getShipSize(ship: Ship) -> int:
  return {
    Ship.SUBMARINE: 1,
    Ship.DESTROYER: 2,
    Ship.CRUISER: 3,
    Ship.BATTLESHIP: 4,
  }[ship]

def getShipCode(ship: Ship) -> str:
  return {
    Ship.SUBMARINE: 'S',
    Ship.DESTROYER: 'D',
    Ship.CRUISER: 'C',
    Ship.BATTLESHIP: 'B',
  }[ship]

def parseData(filename: str) -> tuple[ArrayGrid, list[int], list[int], ShipsRemaining]:
  grid = ArrayGrid(SIZE, SIZE)
  rowspec = []
  colspec = None
  shipsRemainingDict = {
    Ship.BATTLESHIP: 1,
    Ship.CRUISER: 2,
    Ship.DESTROYER: 3,
    Ship.SUBMARINE: 4,
  }

  lines = open(filename).read().splitlines()
  assert len(lines) == SIZE + 1, 'bad input file'

  for y, line in enumerate(lines):
    if y == SIZE:
      colspec = list(map(int, line))
      continue

    assert len(line) == SIZE + 1, 'bad input line'
    for x, c in enumerate(line):
      if x == SIZE:
        rowspec.append(int(c))
        continue

      match c:
        case 'O':
          grid.setValue(x, y, getShipCode(Ship.SUBMARINE))
          shipsRemainingDict[Ship.SUBMARINE] -= 1
        case '|' | '^' | 'v' | '<' | '>' | 'H':
          grid.setValue(x, y, c)
        case '.':
          continue
        case _:
          assert False, 'bad input character: %s' % c

  assert len(rowspec) == SIZE
  assert colspec is not None and len(colspec) == SIZE, 'did not find colspec'
  shipsRemaining = tuple(sorted(shipsRemainingDict.items()))
  assert len(shipsRemaining) == 4, 'bad ships remaining'
  return grid, rowspec, colspec, shipsRemaining

def printGrid(grid: ArrayGrid) -> None:
  grid.print2D({None:'.'})

def printFinalGrid(grid: ArrayGrid) -> None:
  grid.print2D({None:'.', '|': '.'})

def getNumShipsInLine(grid: ArrayGrid, pos: Coords, delta: Delta) -> int:
  px, py = pos
  dx, dy = delta
  assert (dx == 1 or dy == 1) and not (dx == 1 and dy == 1), 'bad delta'

  r = 0
  for i in range(SIZE):
    x, y = px + i * dx, py + i * dy
    if grid.areCoordsWithinBounds(x, y) and grid.getValue(x, y) in ['B', 'C', 'D', 'S']:
      r += 1
  return r

def getNumShipsInRow(grid: ArrayGrid, y: int) -> int:
  return getNumShipsInLine(grid, (0, y), (1, 0))

def getNumShipsInCol(grid: ArrayGrid, x: int) -> int:
  return getNumShipsInLine(grid, (x, 0), (0, 1))

def canPlaceShip(
  grid: ArrayGrid,
  rowspec: list[int],
  colspec: list[int],
  ship: Ship,
  sx: int,
  sy: int,
  orientation: Orientation,
) -> bool:
  dx, dy = (1, 0) if orientation == Orientation.HORIZONTAL else (0, 1)

  shipSize = getShipSize(ship)

  if orientation == Orientation.HORIZONTAL:
    rowsToCheck = [sy]
    colsToCheck = list(range(sx, min(SIZE, sx + shipSize)))
    rowSize = shipSize
    colSize = 1
  else:
    rowsToCheck = list(range(sy, min(SIZE, sy + shipSize)))
    colsToCheck = [sx]
    rowSize = 1
    colSize = shipSize

  for row in rowsToCheck:
    if getNumShipsInRow(grid, row) + rowSize > rowspec[row]:
      return False

  for col in colsToCheck:
    if getNumShipsInCol(grid, col) + colSize > colspec[col]:
      return False

  for i in range(shipSize):
    x, y = sx + i * dx, sy + i * dy
    if not grid.areCoordsWithinBounds(x, y):
      return False

    v = grid.getValue(x, y)
    if v in ['S', 'D', 'C', 'B', WATER]:
      return False
    elif v == '^':
      if not (orientation == Orientation.VERTICAL and i == 0 and shipSize > 1):
        return False
    elif v == 'v':
      if not (orientation == Orientation.VERTICAL and i == shipSize - 1 and shipSize > 1):
        return False
    elif v == '<':
      if not (orientation == Orientation.HORIZONTAL and i == 0 and shipSize > 1):
        return False
    elif v == '>':
      if not (orientation == Orientation.HORIZONTAL and i == shipSize - 1 and shipSize > 1):
        return False
    elif v == 'H':
      if not (i != 0 and i != shipSize - 1 and shipSize > 2):
        return False

    # This ship cannot be placed next to any adjacent ships.
    for _, __, av in grid.getAdjacentItems(x, y, includeDiagonals=True):
      if av in ['S', 'D', 'C', 'B']:
        return False

  return True

def placeShipInAllWays(
  grid: ArrayGrid,
  rowspec: list[int],
  colspec: list[int],
  ship: Ship,
) -> Iterator[ArrayGrid]:
  code = getShipCode(ship)
  size = getShipSize(ship)
  for x in range(SIZE):
    for y in range(SIZE):
      for o in Orientation:
        dx, dy = (1, 0) if o == Orientation.HORIZONTAL else (0, 1)
        if canPlaceShip(grid, rowspec, colspec, ship, x, y, o):
          ngrid = grid.copy()
          for i in range(size):
            nx, ny = x + i * dx, y + i * dy
            ngrid.setValue(nx, ny, code)

            # Place water in surrounding cells.
            for ax, ay, av in ngrid.getAdjacentItems(nx, ny, includeDiagonals=True):
              if av is None:
                # Do not overwrite the new ship with water.
                ngrid.setValue(ax, ay, WATER)

          yield ngrid

def getAdjacentDfsNodes(
  grid: ArrayGrid,
  rowspec: list[int],
  colspec: list[int],
  shipsRemaining: ShipsRemaining,
) -> Iterator[DfsNode]:
  shipsRemainingDict = dict(shipsRemaining)
  shipToPlace = None
  # Process ships in order from largest to smallest.
  for ship in sorted(Ship, reverse=True):
    if shipsRemainingDict[ship] > 0:
      shipToPlace = ship
      break

  if shipToPlace is None:
    print('DONE')
    printFinalGrid(grid)
    return

  if shipToPlace == Ship.SUBMARINE:
    # If we have placed all ships of length two or more, there should not
    # be any ship fragments left over.
    for _, __, value in grid.getItems():
      if value in ['^', 'v', '<', '>', 'H']:
        return

  newShipsRemainingDict = {}
  for ship in shipsRemainingDict:
    newShipsRemainingDict[ship] = shipsRemainingDict[ship] - (1 if ship == shipToPlace else 0)
  newShipsRemaining = tuple(sorted(newShipsRemainingDict.items()))
  assert len(newShipsRemaining) == 4, 'bad number of ships'

  for newGrid in placeShipInAllWays(grid, rowspec, colspec, shipToPlace):
    yield newGrid, newShipsRemaining

def solve(filename: str) -> None:
  grid, rowspec, colspec, shipsRemaining = parseData(filename)

  print('specs:', rowspec, colspec)
  print('ships remaining:', shipsRemaining)
  print('input grid:')
  printGrid(grid)

  getAdj = lambda n: getAdjacentDfsNodes(n[0], rowspec, colspec, n[1])
  dfs((grid, shipsRemaining), getAdj)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('USAGE: %s <input_filename>' % sys.argv[0])
    sys.exit(-1)

  solve(sys.argv[1])
