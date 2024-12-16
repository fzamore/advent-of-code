from typing import Callable, Optional
from common.arraygrid import ArrayGrid

input = open('day15.txt').read().splitlines()

Coords = tuple[int, int]
Delta = tuple[int, int]
GetBoxesToMoveHandler = Callable[[ArrayGrid, Coords, Delta], Optional[list[Coords]]]

def parseInput() -> tuple[ArrayGrid, list[str]]:
  g = []
  movements = []
  for line in input:
    if len(line) == 0:
      continue
    if line[0] in ['.','#','O','@']:
      g.append(line)
    else:
      movements.extend(list(line))
  grid = ArrayGrid.gridFromInput(g, lambda c: c if c != '.' else None)
  return grid, movements

def getDelta(c: str) -> Delta:
  return {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
  }[c]

def findOpenCell(grid: ArrayGrid, pos: Coords, delta: Delta) -> Optional[Coords]:
  x, y = pos
  dx, dy = delta
  while grid.getValue(x, y) == 'O':
    x += dx
    y += dy
  if not grid.hasValue(x, y):
    return x, y
  return None

# Returns an ordered list of box coords to move (in the simple case - does
# not include double boxes). Returns None if the current position can not
# move at all. This is different than returning an empty list; that case
# indicates that the current position can move, but no boxes need to be
# moved.
def getBoxesToMoveSimple(grid: ArrayGrid, pos: Coords, delta: Delta) -> Optional[list[Coords]]:
  cells = []
  x, y = pos
  dx, dy = delta
  while grid.getValue(x, y) in ['[', ']', 'O']: # handles part 1 and part 2
    cells.append((x, y))
    x += dx
    y += dy

  if grid.getValue(x, y) == '#':
    # We hit a wall. We cannot move.
    return None

  assert not grid.hasValue(x, y), 'did not traverse all the way'
  return cells

# Returns an ordered list of box coords to move, but takes into account
# double-boxes.
def getBoxesToMoveComplex(grid: ArrayGrid, pos: Coords, delta: Delta) -> Optional[list[Coords]]:
  toMove = []
  x, y = pos
  _, dy = delta

  # Our queue keeps track of two-cell boxes to move.
  q: list[tuple[int, int, int, int]] = []
  match grid.getValue(x, y):
    case '#':
      return None
    case None:
      return []
    case '[':
      q.append((x, y, x + 1, y))
    case ']':
      q.append((x - 1, y, x, y))
    case _:
      assert False, 'bad value in grid'

  while len(q) > 0:
    x1, y1, x2, y2 = q.pop(0)
    assert grid.getValue(x1, y1) == '[' and grid.getValue(x2, y2) == ']', 'bad box'

    # We don't want to double-move things, as that messes everything up.
    if (x1, y1) not in toMove:
      toMove.append((x1, y1))
    if (x2, y2) not in toMove:
      toMove.append((x2, y2))

    v1, v2 = grid.getValue(x1, y1 + dy), grid.getValue(x2, y2 + dy)
    if v1 == '#' or v2 == '#':
      # We hit a wall. We can't move.
      return None

    # Check both cells in the primary direction of the double-box.
    for x, y, v in [(x1, y1 + dy, v1), (x2, y2 + dy, v2)]:
      if v == '[':
        q.append((x, y, x + 1, y))
      elif v == ']':
        q.append((x - 1, y, x, y))

  return toMove

# Attempts to move the given position in the given direction and returns
# the new position (which may not change).
def tryMove(
  grid: ArrayGrid,
  pos: Coords,
  delta: Delta,
  getCellsToMoveHandler: GetBoxesToMoveHandler,
) -> Coords:
  x, y = pos
  dx, dy = delta
  x += dx
  y += dy

  # Find all the cells we need to move.
  cellsToMove = getCellsToMoveHandler(grid, (x, y), delta)
  if cellsToMove is None:
    # We can't move any cells. Do not move the position.
    return pos

  # Move the cells in reverse order so we don't overwrite anything.
  for cx, cy in cellsToMove[::-1]:
    v = grid.getValue(cx, cy)
    # Move this cell in the primary direction.
    grid.setValue(cx + dx, cy + dy, v)

    # Set the prior location to empty (note that this will often be
    # overwritten in the next iteration).
    grid.setValue(cx, cy, None)

  return x, y

def printGrid(grid: ArrayGrid, pos: Coords) -> None:
  x, y = pos
  assert not grid.hasValue(x, y), 'pos is occupied'
  grid.setValue(x, y, '@')
  grid.print2D({None: '.'})
  grid.setValue(x, y, None)

def iterate(grid: ArrayGrid, movements: list[str], start: Coords, getCellsToMoveHandler: GetBoxesToMoveHandler) -> int:
  print('start:', start)
  grid.setValue(start[0], start[1], None)

  pos = start
  for m in movements:
    pos = tryMove(grid, pos, getDelta(m), getCellsToMoveHandler)
  printGrid(grid, pos)

  ans = 0
  for x, y, v in grid.getItems():
    if v in ['O', '[']: # handles part 1 and part 2
      ans += x + 100 * y
  return ans

def part1() -> None:
  grid, movements = parseInput()

  grid.print2D({None: '.'})
  print('movements:', len(movements))

  start = None
  for x, y, v in grid.getItems():
    if v == '@':
      start = x, y
  assert start is not None, 'did not find start'

  ans = iterate(grid, movements, start, getBoxesToMoveSimple)
  print(ans)

def part2() -> None:
  grid, movements = parseInput()
  print('movements:', len(movements))

  # Embiggen the grid.
  ngrid = ArrayGrid(
    grid.getWidth() * 2,
    grid.getHeight(),
  )

  start = None
  for x, y, v in grid.getItems():
    c1, c2 = None, None
    match v:
      case 'O':
        c1, c2 = '[', ']'
      case '@':
        start = 2 * x, y
      case '#':
        c1, c2 = '#', '#'
      case None:
        pass
      case _:
        assert False, 'bad char %s' % v

    if c1 is not None:
      assert c2 is not None, 'did not find pair of cells'
      ngrid.setValue(2 * x, y, c1)
      ngrid.setValue(2 * x + 1, y, c2)

  def getBoxesToMove(grid: ArrayGrid, pos: Coords, delta: Delta) -> Optional[list[Coords]]:
    _, dy = delta
    return getBoxesToMoveSimple(grid, pos, delta) if dy == 0 else getBoxesToMoveComplex(grid, pos, delta)

  grid = ngrid
  assert start is not None, 'did not find start'
  ans = iterate(grid, movements, start, getBoxesToMove)
  print(ans)

part2()
