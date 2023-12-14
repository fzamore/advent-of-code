from enum import Enum
from math import ceil
from common.arraygrid import ArrayGrid

input = open('day14.txt').read().splitlines()

class Direction(Enum):
  NORTH = 1
  WEST = 2
  SOUTH = 3
  EAST = 4

def initGrid() -> ArrayGrid:
  grid = ArrayGrid(len(input[0]), len(input))
  for y, line in enumerate(input):
    for x, c in enumerate(line):
      grid.setValue(x, y, c)
  return grid

# Tilts the grid in the given direction. This logic was initially
# hardcoded for north, and then extended for all four directions.
def tiltGrid(grid: ArrayGrid, dir: Direction) -> None:
  w, h = grid.getWidth(), grid.getHeight()
  match dir:
    case Direction.NORTH:
      step = 1
      outerRange = range(w)
      innerRange = range(h)
    case Direction.WEST:
      step = 1
      outerRange = range(h)
      innerRange = range(w)
    case Direction.SOUTH:
      step = -1
      outerRange = range(w - 1, -1, -1)
      innerRange = range(h - 1, -1, -1)
    case Direction.EAST:
      step = -1
      outerRange = range(h - 1, -1, -1)
      innerRange = range(w - 1, -1, -1)
    case _:
      assert False, 'bad direction: %s' % dir

  isVert = dir in [Direction.NORTH, Direction.SOUTH]

  for outer in outerRange:
    # keep track of where a rock should slide to
    dst = -1
    for inner in innerRange:
      c = grid.getValue(
        outer if isVert else inner,
        inner if isVert else outer,
      )
      if c == '.' and dst == -1:
        dst = inner
      elif c == '#':
        dst = inner + step
      elif c == 'O':
        if dst != -1 and \
          (step > 0 and dst < inner) or \
          (step < 0 and dst > inner):
          # move rock
          if isVert:
            assert grid.getValue(outer, dst) == '.', \
              'bad spot to move: %d %d %d' % (outer, inner, dst)
            grid.setValue(outer, dst, 'O')
            grid.setValue(outer, inner, '.')
          else:
            assert grid.getValue(dst, outer) == '.', \
              'bad spot to move: %d %d %d' % (inner, outer, dst)
            grid.setValue(dst, outer, 'O')
            grid.setValue(inner, outer, '.')

          # move the destination cell
          dst += step
        else:
          dst = inner + step

def tiltCycle(grid: ArrayGrid) -> None:
  # north, then west, then south, then east
  dirs = [
    Direction.NORTH,
    Direction.WEST,
    Direction.SOUTH,
    Direction.EAST,
  ]
  for dir in dirs:
    tiltGrid(grid, dir)

def computeLoad(grid: ArrayGrid) -> int:
  w, h = grid.getWidth(), grid.getHeight()
  load = 0
  for x in range(w):
    for y in range(h):
      if grid.getValue(x, y) == 'O':
        load += h - y
  return load

def part1():
  grid = initGrid()
  w, h = grid.getWidth(), grid.getHeight()
  print('grid: %d x %d' % (w, h))

  grid.print2D()

  tiltGrid(grid, Direction.NORTH)

  grid.print2D()

  print(computeLoad(grid))

def part2():
  origGrid = initGrid()
  w, h = origGrid.getWidth(), origGrid.getHeight()
  print('grid: %d x %d' % (w, h))

  origGrid.print2D()

  grid = origGrid.copy()
  assert origGrid == grid, 'bad copy'

  gridToCycles = {
    origGrid: 0,
  }
  cyclesToGrid = {
    0: origGrid,
  }

  # cycle the grid once to get started
  tiltCycle(grid)
  assert origGrid != grid, 'bad cycle'

  # Find the number of tilt cycles to find a repeated pattern
  cycles = 1
  while grid not in gridToCycles:
    if cycles % 1000 == 0:
      print(cycles)
      grid.print2D()

    gridToCycles[grid] = cycles
    cyclesToGrid[cycles] = grid
    grid = grid.copy()
    tiltCycle(grid)
    cycles += 1

  firstInPattern = gridToCycles[grid]
  patternLength = cycles - firstInPattern

  grid.print2D()
  print('pattern:', firstInPattern, patternLength)

  # math!
  target = 1000000000
  n = ceil((target - firstInPattern) / patternLength)
  print('n:', n)

  cyclesPastTarget = firstInPattern + n * patternLength - target
  assert cyclesPastTarget < patternLength, 'bad math'
  print('cyclesPastTarget:', cyclesPastTarget)

  cyclesPastStart = patternLength - cyclesPastTarget
  print('cyclesPastStart', cyclesPastStart)
  assert len(gridToCycles) >= cyclesPastStart, 'more bad math'

  gridToCheck = cyclesToGrid[firstInPattern + cyclesPastStart]

  print(computeLoad(gridToCheck))

part2()
