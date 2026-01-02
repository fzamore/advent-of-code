from enum import IntEnum
from typing import Optional, cast
from common.arraygrid import ArrayGrid, turnLeft, turnRight

# This algorithm solves the "Penguin Path" puzzle on the cover of the
# December 2025 issue of GAMES Magazine. The input represents a maze,
# where S is the start and E is the end. Walls are indicated by #. The
# penguin is always in one of three states: a/ only able to go straight at
# green fish (G), b/ only able to turn left at green fish, or c/ only able
# to turn right at green fish. The penguin begins only being able to go
# straight, but whenever he crosses a red fish (R), he must switch to a
# different state.
#
# The solution give in the magazine was a path of length 75, but the
# shortest path I found is of length 71.

data = '''#####E#####
#G GRG G  #
# # #R### #
#  G G   G#
# #R# # # #
#G   G#G G#
# # #R#R# #
#G G G GR #
# # #R# # #
#   #G G  #
#####S#####'''.splitlines()

Coords = tuple[int, int]
class PenguinState(IntEnum):
  STRAIGHT = 1
  LEFT = 2
  RIGHT = 3

# Current position, penguin state, and last position.
PathState = tuple[Coords, PenguinState, Optional[Coords]]

def initGrid() -> ArrayGrid:
  # Python is really dumb sometimes.
  return ArrayGrid.gridFromInput(cast(list[str], data))

def getNextStates(state: PenguinState) -> list[PenguinState]:
  return [s for s in PenguinState if s != state]

def findShortestPath(
  grid: ArrayGrid,
  pos: Coords,
  state: PenguinState,
  lastPos: Optional[Coords] = None,
  pathStates: list[PathState] = [],
) -> Optional[list[Coords]]:
  if (pos, state, lastPos) in pathStates:
    # We've already encountered this state. Stop.
    return None

  x, y = pos
  if not grid.areCoordsWithinBounds(x, y):
    # We've exited the grid. Stop.
    return None
  pathStates.append((pos, state, lastPos))

  v = grid.getValue(x, y)
  if v == '#':
    # We ran into the wall. Stop.
    return None

  if v == 'E':
    return [p[0] for p in pathStates]

  # Keep track of subsequent recursive calls.
  nextCalls: list[tuple[Coords, PenguinState]] = []

  if v == ' ':
    for ax, ay in grid.getAdjacentCoords(x, y):
      nextCalls.append(((ax, ay), state))
  elif v == 'R':
    assert lastPos is not None, 'lastPos not set'
    lx, ly = lastPos
    assert lx == x or ly == y, 'bad movement'
    nx, ny = x + (x - lx), y + (y - ly)
    assert (nx, ny) != lastPos, 'bad movement'
    for nstate in getNextStates(state):
      nextCalls.append(((nx, ny), nstate))
  elif v == 'G':
    assert lastPos is not None, 'lastPos not set'
    lx, ly = lastPos
    dx, dy = x - lx, y - ly
    match state:
      case PenguinState.LEFT:
        dx, dy = turnLeft((dx, dy))
      case PenguinState.RIGHT:
        dx, dy = turnRight((dx, dy))
    nx, ny = x + dx, y + dy
    nextCalls.append(((nx, ny), state))
  else:
    assert False, 'bad grid value'

  shortestLen = 10000
  bestResult = None
  for npos, nstate in nextCalls:
    if npos == lastPos:
      # Don't allow u-turns.
      continue
    result = findShortestPath(grid, npos, nstate, pos, pathStates.copy())
    if result is not None and len(result) < shortestLen:
      shortestLen = len(result)
      bestResult = result
  return bestResult

def printPath(path: list[Coords]) -> None:
  prev = path[0]
  for next in path[1:]:
    px, py = prev
    nx, ny = next
    match (nx - px, ny - py):
      case 1, 0:
        print('>')
      case -1, 0:
        print('<')
      case 0, 1:
        print('v')
      case 0, -1:
        print('^')
      case _:
        assert False, 'bad path'
    prev = next

def solve():
  grid = initGrid()
  print('grid:', grid.getWidth(), grid.getHeight())
  grid.print2D()

  start, end = None, None
  for x, y, v in grid.getItems():
    if v == 'S':
      start = x, y
      grid.setValue(x, y, ' ')
    if v == 'E':
      end = x, y

  assert start is not None, 'did not find start'
  print('start/end:', start, end)
  path = findShortestPath(grid, start, PenguinState.STRAIGHT)
  assert path is not None, 'did not find path'
  print('found shortest path:', len(path))
  # printPath(path)

solve()
