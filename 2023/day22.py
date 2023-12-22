from collections import defaultdict
from copy import deepcopy
from common.sparsegrid import SparseGrid

input = open('day22.txt').read().splitlines()

Coords = tuple[int, int, int]
Brick = tuple[Coords, Coords]

def assertValidBrick(b: Brick) -> None:
  dx = b[1][0] - b[0][0]
  dy = b[1][1] - b[0][1]
  dz = b[1][2] - b[0][2]
  assert b[0][2] > 0 and b[1][2] > 0, \
    'z values should be positive: %s' % str(b)
  assert \
    (dx == 0 and dy == 0) or (dx == 0 and dz == 0)  or (dy == 0 and dz == 0), \
    'invalid brick: %s' % str(b)

def coordRange(b: Brick) -> tuple[range, int]:
  assertValidBrick(b)
  (x1, y1, z1), (x2, y2, z2) = b

  if x1 != x2:
    return range(min(x1, x2), max(x1, x2) + 1), 0

  if y1 != y2:
    return range(min(y1, y2), max(y1, y2) + 1), 1

  if z1 != z2:
    return range(min(z1, z2), max(z1, z2) + 1), 2

  assert False, 'bad brick: %s' % str(b)

def cubesInBrick(b: Brick) -> list[Coords]:
  assertValidBrick(b)

  if b[0] == b[1]:
    # This brick is a single cube.
    return [b[0]]

  cubes = []
  rng, ci = coordRange(b)
  assert b[0][ci] != b[1][ci], 'bad coordRange'
  for i in rng:
    c = {
      0: b[0][0],
      1: b[0][1],
      2: b[0][2],
    }
    c[ci] = i
    cubes.append((c[0], c[1], c[2]))
  return cubes

def canBrickMoveDown(grid: SparseGrid, b: Brick) -> bool:
  cubes = cubesInBrick(b)
  for cube in cubes:
    x, y, z = cube
    assert z > 0, 'bad z coord'
    if z == 1:
      # Brick is on the floor.
      return False

    ncube = x, y, z - 1
    if ncube in cubes:
      # Don't check the grid if the new cube is part of the same brick.
      continue
    if grid.hasValue(ncube):
      # The grid is occupied at this location.
      return False

  return True

def isBrickRestingOnBrick(top: Brick, bottom: Brick) -> bool:
  cubesBottom = cubesInBrick(bottom)
  for x, y, z in cubesInBrick(top):
    if (x, y, z - 1) in cubesBottom:
      return True
  return False

def moveBrickDown(grid: SparseGrid, b: Brick) -> Brick:
  ncubes = []
  for x, y, z in cubesInBrick(b):
    grid.deleteValue((x, y, z))
    ncubes.append((x, y, z - 1))
  for ncube in ncubes:
    assert not grid.hasValue(ncube), 'grid occupied when moving brick down'
    grid.setValue(ncube, 1)
  return (b[0][0], b[0][1], b[0][2] - 1), (b[1][0], b[1][1], b[1][2] - 1)

def initGrid() -> tuple[SparseGrid, dict[int, Brick]]:
  grid = SparseGrid(3)
  bricks = {}
  for i, line in enumerate(input):
    v = line.split('~')
    x1, y1, z1 = map(int, v[0].split(','))
    x2, y2, z2 = map(int, v[1].split(','))
    b = ((x1, y1, z1), (x2, y2, z2))
    assertValidBrick(b)

    bricks[i] = b

    brickCubes = cubesInBrick(b)
    print('brick cubes:', b, len(brickCubes), brickCubes)
    for cube in brickCubes:
      grid.setValue(cube, 1)

  return grid, bricks

def moveBricksDown(grid: SparseGrid, bricks: dict[int, Brick]) \
  -> dict[int, Brick]:
  while True:
    bricksToMove = {}
    nbricks = {}
    for id1 in bricks:
      brick = bricks[id1]

      # store bricks for next iteration
      nbricks[id1] = brick

      if canBrickMoveDown(grid, brick):
        bricksToMove[id1] = brick

    if len(bricksToMove) == 0:
      break

    for id1 in bricksToMove:
      brick = bricksToMove[id1]
      nbricks[id1] = moveBrickDown(grid, brick)

    bricks = nbricks
  return bricks

# Removes a brick and returns the number of other bricks that would
# subsequently fall.
def removeBrick(
  bricks: dict[int, Brick],
  brickId: int,
  forwardDependencies: dict[int, set[int]],
  reverseDependencies: dict[int, set[int]],
) -> int:
  result = 0
  r = reverseDependencies[brickId].copy()
  for id1 in r:
    assert brickId in forwardDependencies[id1], 'bad dependency map'

    # Remove bricks from the map.
    forwardDependencies[id1].remove(brickId)
    reverseDependencies[brickId].remove(id1)

    if len(forwardDependencies[id1]) == 0:
       # The last supporting brick was removed, so cascade the removal.
       # Add one to the result to account for this brick that was removed.
      result += 1 + \
        removeBrick(bricks, id1, forwardDependencies, reverseDependencies)
  return result

def part1() -> None:
  grid, bricks = initGrid()
  print('bricks:', len(bricks))

  bricks = moveBricksDown(grid, bricks)

  bricksCanDisintegrate = {}
  for id1 in bricks:
    # Delete the brick from the grid and check if any other bricks can fall.
    cubes = cubesInBrick(bricks[id1])
    for cube in cubes:
      grid.deleteValue(cube)

    canDisintegrate = True
    for id2 in bricks:
      if id1 == id2:
        continue
      if canBrickMoveDown(grid, bricks[id2]):
        # Another brick can move down. The original brick cannot be disintegrated.
        canDisintegrate = False
    if canDisintegrate:
      bricksCanDisintegrate[id1] = bricks[id1]

    # Put the brick back in the grid for the next iteration.
    for cube in cubes:
      grid.setValue(cube, 1)

  print(len(bricksCanDisintegrate))

def part2() -> None:
  grid, bricks = initGrid()
  print('bricks:', len(bricks))

  bricks = moveBricksDown(grid, bricks)

  # Build forward- and reverse-dependency maps.
  print('building dependencies')
  forwardDependencies = defaultdict(set)
  reverseDependencies = defaultdict(set)
  for id1 in bricks:
      for id2 in bricks:
        if id1 == id2:
          continue
        if isBrickRestingOnBrick(bricks[id1], bricks[id2]):
          forwardDependencies[id1].add(id2)
          reverseDependencies[id2].add(id1)

  print('removing bricks')
  count = 0
  for id in bricks:
    count += removeBrick(
      bricks,
      id,
      deepcopy(forwardDependencies),
      deepcopy(reverseDependencies),
    )
  print(count)

part2()
