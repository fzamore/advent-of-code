from enum import IntEnum
from typing import Iterable, Optional, cast
from common.arraygrid import ArrayGrid, turnLeft, turnRight
from common.shortestpath import dijkstraAllShortestPaths

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

def getNextPathStates(grid: ArrayGrid, pathState: PathState) -> Iterable[PathState]:
  pos, penguinState, lastPos = pathState
  x, y = pos
  assert grid.areCoordsWithinBounds(x, y), 'moved beyond grid'

  match grid.getValue(x, y):
    case '#':
      # We ran into the wall. Stop.
      pass

    case ' ' | 'S':
      # Empty cell (or start). Choose any direction except the one we came from.
      for ax, ay in grid.getAdjacentCoords(x, y):
        if (ax, ay) == lastPos:
          # No u-turns.
          continue
        yield ((ax, ay), penguinState, pos)

    case 'R':
      # Red fish. Go straight, but change state.
      assert lastPos is not None, 'lastPos not set'
      lx, ly = lastPos
      assert lx == x or ly == y, 'can only move orthogonally one space at a time'
      nx, ny = x + (x - lx), y + (y - ly)
      assert (nx, ny) != lastPos, 'illegal u-turn'
      for nstate in PenguinState:
        if nstate != penguinState:
          yield ((nx, ny), nstate, pos)

    case 'G':
      # Green fish. Move in the direction dicated by the state.
      assert lastPos is not None, 'lastPos not set'
      lx, ly = lastPos
      dx, dy = x - lx, y - ly
      match penguinState:
        case PenguinState.LEFT:
          dx, dy = turnLeft((dx, dy))
        case PenguinState.RIGHT:
          dx, dy = turnRight((dx, dy))
      yield ((x + dx, y + dy), penguinState, pos)
    case _:
      assert False, 'bad grid value'

def findShortestPathDfs(
  grid: ArrayGrid,
  pos: Coords,
  penguinState: PenguinState = PenguinState.STRAIGHT,
  lastPos: Optional[Coords] = None,
  pathStates: list[PathState] = [],
) -> Optional[list[Coords]]:
  if (pos, penguinState, lastPos) in pathStates:
    # We've already encountered this state. Stop.
    return None

  x, y = pos
  pathStates.append((pos, penguinState, lastPos))

  assert grid.areCoordsWithinBounds(x, y), 'moved beyond grid'
  if grid.getValue(x, y) == 'E':
    return [p[0] for p in pathStates]

  shortestLen = 100000000
  bestResult = None
  for (npos, nstate, nLastPos) in getNextPathStates(grid, (pos, penguinState, lastPos)):
    result = findShortestPathDfs(grid, npos, nstate, nLastPos, pathStates.copy())
    if result is not None and len(result) < shortestLen:
      shortestLen = len(result)
      bestResult = result
  return bestResult

def findShortestPathDijkstra(grid: ArrayGrid, start: Coords) -> list[Coords]:
  def getAdj(pathState: PathState) -> Iterable[tuple[PathState, int]]:
    for nextPathState in getNextPathStates(grid, pathState):
      yield nextPathState, 1

  def isDone(pathState: PathState) -> bool:
    (x, y), _, _ = pathState
    return grid.getValue(x, y) == 'E'

  startState: PathState = (start, PenguinState.STRAIGHT, None)
  result = dijkstraAllShortestPaths(startState, getAdj, isDone)
  allPaths = list(result[2])
  assert len(allPaths) > 0, 'did not find a path'

  # Arbitrarily return the first path.
  return [p[0] for p in allPaths[0]]

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

def solve() -> None:
  grid = initGrid()
  print('grid:', grid.getWidth(), grid.getHeight())
  grid.print2D()

  start, end = None, None
  for x, y, v in grid.getItems():
    if v == 'S':
      start = x, y
    if v == 'E':
      end = x, y

  assert start is not None, 'did not find start'
  print('start/end:', start, end)
  pathDfs = findShortestPathDfs(grid, start)
  assert pathDfs is not None, 'did not find path'
  print('found shortest path:', len(pathDfs))

  pathDijkstra = findShortestPathDijkstra(grid, start)
  print('found shortest path via dijkstra:', len(pathDijkstra))

  assert len(pathDfs) == len(pathDijkstra), 'two algorithms did not find same shortest path'

  # printPath(path)

solve()
