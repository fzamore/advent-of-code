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
    # The beam has exited the grid. No need to trace it further.
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

# Traces a single beam through the grid to its completion (either exiting
# the grid or looping indefinitely).
def traceBeam(grid: ArrayGrid, beam: Beam, beamSet: set[Beam]) -> None:
  if beam in beamSet:
    return

  if grid.areCoordsWithinBounds(beam.x, beam.y):
    # Make sure the beam is within the grid before adding it. Only an
    # issue with the start beam.
    beamSet.add(beam)
  else:
    assert beam.x == -1 or beam.y == -1 or \
      beam.x == grid.getWidth() or beam.y == grid.getHeight(), \
      'beam outside grid should be just along border: %s' % str(beam)

  beams = iterateBeam(grid, beam)
  while len(beams) > 0:
    b = beams.pop()
    if b in beamSet:
      # We've already seen this beam. No need to trace it further.
      continue

    assert grid.areCoordsWithinBounds(b.x, b.y), 'iterated beam beyond grid'
    beamSet.add(b)
    beams.extend(iterateBeam(grid, b))

def beamSetToTileCount(beamSet: set[Beam]) -> int:
  # Some coordinates may appear in the beam set multiple times, because
  # there may be beams in the same positions going in different
  # directions. Dedup them here by (x, y) coordinate.
  return len(set([(b.x, b.y) for b in beamSet]))

def beamsToPrint(beamSet: set[Beam]) -> dict[tuple[int, int], str]:
  b = {
    (1, 0): '>',
    (-1, 0): '<',
    (0, 1): 'v',
    (0, -1): '^',
  }
  d = {}
  for beam in beamSet:
    d[(beam.x, beam.y)] = b[beam.delta]
  return d

def computeEnergizedTileCount(grid: ArrayGrid, startBeam: Beam) -> int:
  beamSet: set[Beam] = set()
  traceBeam(grid, startBeam, beamSet)
  return beamSetToTileCount(beamSet)

def printBeamGrid(grid: ArrayGrid, beamSet: set[Beam]) -> None:
  d = beamsToPrint(beamSet)

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

def printEnergizedGrid(grid: ArrayGrid, beamSet: set[Beam]) -> None:
  d = beamsToPrint(beamSet)

  print()
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      if (x, y) in d:
        print('#', end='')
      else:
        print('.', end='')
    print()
  print()

def part1() -> None:
  grid = initGrid()
  print('grid size: %d x %d' % (grid.getWidth(), grid.getHeight()))

  startBeam = Beam(-1, 0, (1, 0))

  beamSet: set[Beam] = set()
  traceBeam(grid, startBeam, beamSet)

  printBeamGrid(grid, beamSet)
  printEnergizedGrid(grid, beamSet)

  print(beamSetToTileCount(beamSet))

def part2() -> None:
  grid = initGrid()
  w, h = grid.getWidth(), grid.getHeight()
  print('grid size: %d x %d' % (w, h))

  startBeams = []
  for x in range(w):
    startBeams.append(Beam(x, -1, (0, 1)))
    startBeams.append(Beam(x, h, (0, -1)))
  for y in range(h):
    startBeams.append(Beam(-1, y, (1, 0)))
    startBeams.append(Beam(w, y, (-1, 0)))

  result = -1
  for startBeam in startBeams:
    print('start beam: (%d, %d)' % (startBeam.x, startBeam.y))
    r = computeEnergizedTileCount(grid, startBeam)
    result = max(result, r)
    print('  results:', r, result)

  print(result)

part2()
