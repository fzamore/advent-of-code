from collections import namedtuple
from common.arraygrid import ArrayGrid

input = open('day16.txt').read().splitlines()

Beam = namedtuple('Beam', ['x', 'y', 'delta'])

def iterateBeam(grid: ArrayGrid, beam: Beam) -> set[Beam]:
  x, y, delta = beam
  assert delta in [(1, 0), (-1, 0), (0, 1), (0, -1)], 'bad delta'
  dx, dy = delta
  nx, ny = x + dx, y + dy
  if not grid.areCoordsWithinBounds(nx, ny):
    return set()

  tile = grid.getValue(nx, ny)
  match tile:
    case '.':
      return set([Beam(nx, ny, delta)])
    case '/':
      return set([Beam(nx, ny, (-dy, -dx))])
    case '\\':
      return set([Beam(nx, ny, (dy, dx))])
    case '-':
      if delta in [(1, 0), (-1, 0)]:
        return set([Beam(nx, ny, delta)])
      else:
        return set([
          Beam(nx, ny, (dy, dx)),
          Beam(nx, ny, (-dy, dx))
        ])
    case '|':
      if delta in [(0, 1), (0, -1)]:
        return set([Beam(nx, ny, delta)])
      else:
        return set([
          Beam(nx, ny, (dy, dx)),
          Beam(nx, ny, (dy, -dx))
        ])
    case _:
      assert False, 'bad tile: %s' % tile

def iterateGrid(grid: ArrayGrid, beams: set[Beam]) -> set[Beam]:
  resultBeams: set[Beam] = set()
  for beam in beams:
    resultBeams = resultBeams.union(iterateBeam(grid, beam))
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

def initGrid() -> ArrayGrid:
  w, h = len(input[0]), len(input)
  grid = ArrayGrid(w, h)
  for y in range(h):
    for x in range(w):
      grid.setValue(x, y, input[y][x])
  return grid

# this takes ~45 seconds to run
def part1():
  grid = initGrid()
  print('%d x %d' % (grid.getWidth(), grid.getHeight()))

  startBeam = Beam(-1, 0, (1, 0))

  beams = set([startBeam])
  allBeams = beams.copy()
  while True:
    beams = iterateGrid(grid, beams)
    if allBeams.union(beams) == allBeams:
      break
    allBeams = allBeams.union(beams)
    print('beam count:', len(beams), len(allBeams))
  printBeamGrid(grid, allBeams)
  printEnergizedGrid(grid, allBeams)

  energizedTiles = set()
  for x, y, _ in allBeams:
    if grid.areCoordsWithinBounds(x, y):
      energizedTiles.add((x, y))
  print(len(energizedTiles))

part1()
