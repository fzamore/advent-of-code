from collections import namedtuple
from common.sparsegrid import SparseGrid

input = open('day17.txt').read().splitlines()[0]
WIDTH = 7

# Coordinate system: +y is up.

Rock = namedtuple('Rock', [
  'points', # list of all points
  'left', # leftmost point, relative to bottom
  'top', # top point, relative to bottom
])
rocks = [
  Rock([(0, 0), (1, 0), (2, 0), (3, 0)], (0, 0), (0, 0)),
  Rock([(0, 0), (-1, 1), (0, 1), (1, 1), (0, 2)], (-1, 1), (0, 2)),
  Rock([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], (0, 0), (2, 2)),
  Rock([(0, 0), (0, 1), (0, 2), (0, 3)], (0, 0), (0, 3)),
  Rock([(0, 0), (1, 0), (0, 1), (1, 1)], (0, 0), (0, 1)),
]

def computeRockPositions(
  rock: Rock,
  bottomPoint: tuple[int, int],
) -> list[tuple[int, int]]:
  px, py = bottomPoint
  return [(px + p[0], py + p[1]) for p in rock.points]

def canMove(
  cave: SparseGrid,
  rock: Rock,
  bottomPoint: tuple[int, int],
  delta: tuple[int, int],
) -> bool:
  assert delta in [(0, -1), (-1, 0), (1, 0)]
  px, py = bottomPoint
  dx, dy = delta
  for x, y in rock.points:
    nx, ny = (px + x + dx, py + y + dy)
    if nx < 0 or nx >= WIDTH:
      return False
    if cave.hasValue((nx, ny)):
      return False
  return True

# Tries to move the rock by the given delta. Returns the new bottom point,
# which will be the same if the rock was unable to move.
def tryMoveRock(
  cave: SparseGrid,
  rock: Rock,
  bottomPoint: tuple[int, int],
  delta: tuple[int, int],
) -> tuple[int, int]:
  px, py = bottomPoint
  dx, dy = delta
  if canMove(cave, rock, bottomPoint, delta):
    bottomPoint = (px + dx, py + dy)
  return bottomPoint

def storeRock(
  cave: SparseGrid,
  rock: Rock,
  bottomPoint: tuple[int, int],
) -> None:
  rockPositions = computeRockPositions(rock, bottomPoint)
  for x, y in rockPositions:
    assert not cave.hasValue((x, y)), 'cave already has rock at %d, %d' % (x, y)
    cave.setValue((x, y), '#')

def printCave(
  cave: SparseGrid,
  height: int,
  fallingRockPositions: list[tuple[int, int]] = [],
  yBounds: tuple[int, int] = (-1, -1),
) -> None:
  if yBounds[1] == -1:
    yBounds = (-1, height - 1)
  print()
  for y in range(yBounds[1], yBounds[0] - 1, -1):
    for x in range(-1, WIDTH + 1):
      if x == -1 or x == WIDTH:
        if y == -1:
          print('+', end='')
        else:
          print('|', end='')
      else:
        if (x, y) in fallingRockPositions:
          print('@', end='')
        else:
          print(cave.getValue((x, y), '.'), end='')
    print()
  print()

# Returns the contour at the top of the cave. Return value is always a
# seven-length tuple, the first element is always 0. The next six elements
# are the y-positions of the top of of the cave at that x-position,
# relative to the first element.
def getCaveTopPattern(
  cave: SparseGrid,
  caveTop: int,
) -> tuple[int, ...]:
  # Leftmost value is always 0, and everything after is relative to that.
  result = [0]
  for x in range(0, WIDTH):
    y = caveTop
    while not cave.hasValue((x, y)):
      y -= 1
    if x == 0:
      baseY = y
    else:
      result.append(y - baseY)
  assert len(result) == 7
  return tuple(result)

def part1():
  cave = SparseGrid(2)
  caveTop = -1
  # Add bottom of cave.
  for i in range(WIDTH):
    cave.setValue((i, -1), '-')

  ji = 0
  count = 2022
  for i in range(count):
    rock = rocks[i % len(rocks)]
    bottomPoint = (2 - rock.left[0], caveTop + 4)
    while True:
      # Move via the jet.
      jet = input[ji % len(input)]
      ji += 1
      assert jet in ['<', '>'], 'bad jet: %s' % jet
      delta = {'<': (-1, 0), '>': (1, 0)}[jet]
      bottomPoint = tryMoveRock(cave, rock, bottomPoint, delta)

      # Move via gravity.
      delta = (0, -1)
      np = tryMoveRock(cave, rock, bottomPoint, (0, -1))
      if np == bottomPoint:
        # The rock has come to rest.
        storeRock(cave, rock, bottomPoint)

        rockHeight = rock.top[1] + 1
        # The top should never shrink.
        caveTop = max(caveTop, rockHeight + bottomPoint[1] - 1)
        break
      bottomPoint = np

  print(caveTop + 1)

def part2():
  patternLength = len(input)
  print('jet pattern length:', patternLength)

  cave = SparseGrid(2)
  caveTop = -1
  # Add bottom of cave.
  for i in range(WIDTH):
    cave.setValue((i, -1), '-')

  # The cave top pattens. The key is described below.
  caveTopPatterns = {}

  # The cave top after each rock lands.
  caveTops = {}

  jpos = 0
  print()
  i = 0
  while True:
    rock = rocks[i % len(rocks)]
    bottomPoint = (2 - rock.left[0], caveTop + 4)
    while True:
      # Move via the jet.
      jet = input[jpos % len(input)]
      jpos += 1
      assert jet in ['<', '>'], 'bad jet: %s' % jet
      delta = {'<': (-1, 0), '>': (1, 0)}[jet]
      bottomPoint = tryMoveRock(cave, rock, bottomPoint, delta)

      # Move via gravity.
      delta = (0, -1)
      np = tryMoveRock(cave, rock, bottomPoint, (0, -1))
      if np == bottomPoint:
        # The rock has come to rest.
        storeRock(cave, rock, bottomPoint)

        rockHeight = rock.top[1] + 1
        # The top should never shrink.
        caveTop = max(caveTop, rockHeight + bottomPoint[1] - 1)
        caveTops[i] = caveTop
        break
      bottomPoint = np

    # The goal is to find a recurring pattern, given a unique combination of:
    # - rock number
    # - jet position
    # - cave-top pattern
    # If these three things are the same, then we will have a repeating pattern.
    # Given such a pattern, we want to determine:
    # - the configuration at the start of the pattern
    # - how many rocks are dropped during each pattern
    # - most importantly: how far the top of the cave rises during each pattern
    caveTopPatternKey = (
      i % len(rocks),
      jpos % len(input),
      getCaveTopPattern(cave, caveTop),
    )
    if caveTopPatternKey in caveTopPatterns:
      # We have found the end of the first occurrence of the pattern. Stop
      # dropping rocks.
      break
    # Store the rock index for this pattern at each dropped rock.
    caveTopPatterns[caveTopPatternKey] = i

    i += 1

  # The rock index at the start of the pattern.
  firstRockI = caveTopPatterns[caveTopPatternKey] + 1
  # The rock index at the end of the pattern.
  lastRockI = i
  rocksPerPattern = lastRockI - firstRockI + 1
  print('firstRockI:', firstRockI)
  print('lastRockI:', lastRockI)
  print('rocksPerPattern:', rocksPerPattern)
  assert len(caveTops) >= rocksPerPattern

  # The amount the cave top rises per pattern.
  assert caveTops[i] == caveTop
  caveTopChangePerPattern = caveTops[i] - caveTops[firstRockI - 1]
  print('caveTopChangePerPattern:', caveTopChangePerPattern)

  # Assume the pattern starts at firstRockI. Thus, we need to see how many
  # times the pattern repeats starting at that rock.
  totalRocks = 1000000000000 - firstRockI

  # The number of complete patterns we need.
  numCompletePatterns = totalRocks // rocksPerPattern
  # The number of rocks we need to drop after the last pattern has completed.
  leftOverRocks = totalRocks % rocksPerPattern

  # The top of the cave at the end of the last complete pattern.
  caveTopAtEndOfLastPattern = numCompletePatterns * caveTopChangePerPattern

  print('numPatterns:', numCompletePatterns)
  print('leftOverRocks:', leftOverRocks)
  print('caveTopAtEndOfLastPattern:', caveTopAtEndOfLastPattern)

  assert rocksPerPattern * numCompletePatterns + leftOverRocks == totalRocks

  # The answer is the sum of the following:
  # - the caveTop at the first rock of the pattern.
  # - the caveTop at the end of the last complete pattern
  #   (the pattern starts at firstRockI)
  # - the change in caveTop over the first "leftOverRocks" of the pattern
  print(
    caveTops[firstRockI] + \
    caveTopAtEndOfLastPattern + \
    caveTops[firstRockI + leftOverRocks] - caveTops[firstRockI],
  )

part2()
