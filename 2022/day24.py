from common.arraygrid import ArrayGrid
from common.shortestpath import dijkstra

input = open('day24.txt').read().splitlines()

Coords = tuple[int, int]
Delta = tuple[int, int]
Node = tuple[Coords, int]

def createEmptyGrid(width: int, height: int) -> ArrayGrid:
  grid = ArrayGrid(width, height)
  for x in range(width):
    for y in range(height):
      grid.setValue(x, y, [])
  return grid

def initGrid() -> ArrayGrid:
  width = len(input[0]) - 2
  height = len(input) - 2

  grid = createEmptyGrid(width, height)

  for y in range(height):
    for x in range(width):
      c = input[y + 1][x + 1]
      if x == 0 or x == width - 1:
        assert c != 'v' and c != '^', \
          'cannot have vertical blizzard in first or last column'
      if c != '.':
        grid.getValue(x, y).append(c)

  return grid

def printGrid(grid: ArrayGrid, pos: Coords | None = None) -> None:
  print()
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      if (x, y) == pos:
        assert len(grid.getValue(x, y)) == 0, \
          'current pos is occupied: (%d, %d): %s' % (x, y, grid.getValue(x, y))
        print('E', end='')
        continue
      v = grid.getValue(x, y)
      assert isinstance(v, list)
      match len(v):
        case 0: p = '.'
        case 1: p = v[0]
        case _: p = str(len(v))
      print(p, end='')
    print()
  print()

def getNextCell(
  grid: ArrayGrid,
  coords: Coords,
  delta: Delta,
) -> Coords:
  width, height = grid.getWidth(), grid.getHeight()
  x, y = coords
  dx, dy = delta
  return (x + dx) % width, (y + dy) % height

def iterateBlizzards(grid: ArrayGrid) -> ArrayGrid:
  width, height = grid.getWidth(), grid.getHeight()
  ngrid = createEmptyGrid(width, height)
  for y in range(height):
    for x in range(width):
      for blizzard in grid.getValue(x, y):
        match blizzard:
          case '<': nx, ny = getNextCell(grid, (x, y), (-1, 0))
          case '>': nx, ny = getNextCell(grid, (x, y), (1, 0))
          case '^': nx, ny = getNextCell(grid, (x, y), (0, -1))
          case 'v': nx, ny = getNextCell(grid, (x, y), (0, 1))
          case _: assert False, 'invalid value at (%d, %d)' % (x, y)
        ngrid.getValue(nx, ny).append(blizzard)

  return ngrid

def part1():
  grid = initGrid()

  width, height = grid.getWidth(), grid.getHeight()
  print('width x height:', width, height)

  startPos = (0, -1)

  # Approach: run Dijkstra over the grid, but each node is an (x, y, t)
  # tuple, where t is the minutes elapsed so far. When determining
  # neighbors, get the state of the grid at time t + 1, and return all
  # possible moves in that grid (including not changing positions).

  # precompute grid iterations (400 is an upper bound determined by
  # previous failed approaches).
  gridIterations: dict[int, ArrayGrid] = {
     0: grid,
  }
  for i in range(1, 400):
    gridIterations[i] = iterateBlizzards(gridIterations[i - 1])

  def getAdjacent(node: Node) -> list[tuple[Node, int]]:
    (x, y), minutesElapsed = node

    grid = gridIterations[minutesElapsed]
    assert grid is not None

    neighbors = []
    for dx, dy in [(1, 0), (0, 1), (0, 0), (-1, 0), (0, -1)]:
      nx, ny = x + dx, y + dy
      # special-case waiting in the start position (because its position
      # is technically outside the grid)
      if (nx, ny) == startPos and (dx, dy) == (0, 0):
        neighbors.append((nx, ny))
        continue

      if not grid.areCoordsWithinBounds(nx, ny):
        continue

      if len(grid.getValue(nx, ny)) == 0:
        neighbors.append((nx, ny))

    return [((pos, minutesElapsed + 1), 1) for pos in neighbors]

  def isDone(node: Node) -> bool:
    (x, y), _ = node
    return x == width - 1 and y == height - 1

  ((x, y), _), score = dijkstra(
    (startPos, 0),
    getAdjacent,
    isDone,
  )
  print(x, y)
  print(score)

part1()

