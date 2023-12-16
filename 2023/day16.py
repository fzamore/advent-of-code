from collections import namedtuple
from common.arraygrid import ArrayGrid

input = open('day16.txt').read().splitlines()

Beam = namedtuple('Beam', ['x', 'y', 'delta'])

def initGrid() -> ArrayGrid:
  w, h = len(input[0]), len(input)
  grid = ArrayGrid(w, h)
  for y in range(h):
    for x in range(w):
      grid.setValue(x, y, input[y][x])
  return grid

# Iterates the given bean one step and returns the resulting active beams
# (either 0, 1, or 2).
def iterateBeam(grid: ArrayGrid, beam: Beam) -> list[Beam]:
  x, y, delta = beam
  assert delta in [(1, 0), (-1, 0), (0, 1), (0, -1)], 'bad delta'
  dx, dy = delta
  nx, ny = x + dx, y + dy
  if not grid.areCoordsWithinBounds(nx, ny):
    return []

  tile = grid.getValue(nx, ny)
  match tile:
    case '.':
      return [Beam(nx, ny, delta)]
    case '/':
      return [Beam(nx, ny, (-dy, -dx))]
    case '\\':
      return [Beam(nx, ny, (dy, dx))]
    case '-':
      if delta in [(1, 0), (-1, 0)]:
        return [Beam(nx, ny, delta)]
      else:
        return [
          Beam(nx, ny, (dy, dx)),
          Beam(nx, ny, (-dy, dx))
        ]
    case '|':
      if delta in [(0, 1), (0, -1)]:
        return [Beam(nx, ny, delta)]
      else:
        return [
          Beam(nx, ny, (dy, dx)),
          Beam(nx, ny, (dy, -dx))
        ]
    case _:
      assert False, 'bad tile: %s' % tile

# Iterates each given beam in the grid by one step. Returns the new active
# beams after the iteration.
def iterateGrid(grid: ArrayGrid, beams: set[Beam]) -> set[Beam]:
  resultBeams = set()
  for beam in beams:
    resultBeams.update(iterateBeam(grid, beam))
  return resultBeams

def beamsToPrint(beams: set[Beam]) -> dict[tuple[int, int], str]:
  b = {
    (1, 0): '>',
    (-1, 0): '<',
    (0, 1): 'v',
    (0, -1): '^',
  }
  d = {}
  for beam in beams:
    d[(beam.x, beam.y)] = b[beam.delta]
  return d

def printBeamGrid(grid: ArrayGrid, beams: set[Beam]) -> None:
  d = beamsToPrint(beams)

  print()
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      c = grid.getValue(x, y)
      if (x, y) in d and c == '.':
        print(d[(x, y)], end='')
      else:
        print(c, end='')
    print()
  print()

def printEnergizedGrid(grid: ArrayGrid, beams: set[Beam]) -> None:
  d = beamsToPrint(beams)

  print()
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      if (x, y) in d:
        print('#', end='')
      else:
        print('.', end='')
    print()
  print()

def part1():
  grid = initGrid()
  print('grid size: %d x %d' % (grid.getWidth(), grid.getHeight()))

  startBeam = Beam(-1, 0, (1, 0))

  beams = set([startBeam])
  allBeams = beams.copy()
  while True:
    allBeamsCount = len(allBeams)
    beams = iterateGrid(grid, beams)
    allBeams.update(beams)
    if len(allBeams) == allBeamsCount:
      # We didn't add any new beams. Stop.
      break
  printBeamGrid(grid, allBeams)
  printEnergizedGrid(grid, allBeams)

  energizedTiles = set()
  for x, y, _ in allBeams:
    if grid.areCoordsWithinBounds(x, y):
      energizedTiles.add((x, y))
  print(len(energizedTiles))

part1()
