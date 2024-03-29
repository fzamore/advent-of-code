from common.arraygrid import ArrayGrid
from common.shortestpath import dijkstraAllNodes

input = open('day17.txt').read().splitlines()

Coords = tuple[int, int]

# We store a state as a (Coords, isHorizontal) tuple that represents a
# given node and whether we're moving horizontally or vertically.
State = tuple[Coords, bool]

def getNextStates(
  grid: ArrayGrid,
  startNode: Coords,
  state: State,
  minStepCount: int = 1,
  maxStepCount: int = 3,
) -> list[tuple[State, int]]:
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
  # line, and since we begin by going right and down 1, 2, and 3 steps
  # from the start node, this process is guaranteed to encounter every
  # cell in the grid.
  results = []
  for dx, dy in deltas:
    value = 0
    # If minStepCount > 1, we need to add values before any valid moves.
    for i in range(1, minStepCount):
      nx, ny = x + i * dx, y + i * dy
      if grid.areCoordsWithinBounds(nx, ny):
        value += grid.getValue(nx, ny)
    for i in range(minStepCount, maxStepCount + 1):
      nx, ny = x + i * dx, y + i * dy
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
  print('grid: %d x %d' % (w, h))
  grid.print2D()

  startNode = (0, 0)
  endNode = (w - 1, h - 1)

  startState = (startNode, True) # isHoriz doesn't matter for the start node
  results = dijkstraAllNodes(startState, lambda s: getNextStates(grid, startNode, s))
  # Find the minimum result that includes the end node.
  print(min(results[s] for s in results if s[0] == endNode))

def part2() -> None:
  grid = ArrayGrid.gridFromInput(input, lambda x: int(x))
  w, h = grid.getWidth(), grid.getHeight()
  print('grid: %d x %d' % (w, h))
  grid.print2D()

  startNode = (0, 0)
  endNode = (w - 1, h - 1)

  startState = (startNode, True) # isHoriz doesn't matter for the start node
  results = dijkstraAllNodes(
    startState,
    lambda s: getNextStates(grid, startNode, s, 4, 10),
  )
  print(min(results[s] for s in results if s[0] == endNode))

part2()
