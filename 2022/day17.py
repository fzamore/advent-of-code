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
  ) -> None:
  print()
  for y in range(height - 1, -2, -1):
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

def part1():
  rocks = [
    Rock([(0, 0), (1, 0), (2, 0), (3, 0)], (0, 0), (0, 0)),
    Rock([(0, 0), (-1, 1), (0, 1), (1, 1), (0, 2)], (-1, 1), (0, 2)),
    Rock([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], (0, 0), (2, 2)),
    Rock([(0, 0), (0, 1), (0, 2), (0, 3)], (0, 0), (0, 3)),
    Rock([(0, 0), (1, 0), (0, 1), (1, 1)], (0, 0), (0, 1)),
  ]

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

part1()
