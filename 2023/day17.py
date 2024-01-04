from common.arraygrid import ArrayGrid
from common.shortestpath import dijkstraAllNodes

input = open('day17.txt').read().splitlines()

Coords = tuple[int, int]

# We store a state as a (Coords, isHorizontal) tuple.
State = tuple[Coords, bool]

def getNextStates(grid: ArrayGrid, startNode: Coords, state: State) -> \
  list[tuple[State, int]]:
  (x, y), isHoriz = state

  if isHoriz:
    deltas = [(0, 1), (0, -1)]
  else:
    deltas = [(1, 0), (-1, 0)]

  # Special-case the start node to go both horizontally and vertically.
  if (x, y) == startNode:
    deltas = [(1, 0), (0, 1)]

  # I stole this from Reddit.
  #
  # Compute the next possible states by first turning 90 degrees and
  # moving 1, 2 or 3 steps in that direction (this requires that we store
  # in each state whether we're moving horizontally or vertically). Since
  # we turn both left and right, this process results in a maximum of 6
  # possible next states. The value of each state is the sum of the grid
  # values along the path (up to three values). By first turning, we
  # eliminate the possibility of going more than 3 steps in a straight
  # line, and since we start by going right and down 1, 2, and 3 steps
  # from the start, this process is guaranteed to hit every cell in the
  # grid.
  stepCount = 3
  results = []
  for dx, dy in deltas:
    value = 0
    for i in range(stepCount):
      nx, ny = x + (i + 1) * dx, y + (i + 1) * dy
      if not grid.areCoordsWithinBounds(nx, ny):
        continue
      value += grid.getValue(nx, ny)
      newIsHoriz = dx != 0
      newState = (nx, ny), newIsHoriz
      results.append((newState, value))

  return results

def part1() -> None:
  grid = ArrayGrid.gridFromInput(input, lambda x: int(x))
  w, h = grid.getWidth(), grid.getHeight()
  assert w == h, 'not a square'
  print('grid: %d x %d' % (w, h))
  grid.print2D()

  startNode = (0, 0)
  endNode = (w - 1, h - 1)

  startState = (startNode, True) # isHoriz doesn't matter for the start node
  results = dijkstraAllNodes(startState, lambda s: getNextStates(grid, startNode, s))
  print(min(results[s] for s in results if s[0] == endNode))

part1()
