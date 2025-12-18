from common.arraygrid import ArrayGrid
from common.ints import ints

data = open('day12.txt').read().splitlines()
N = 3

Coords = tuple[int, int]
Shape = ArrayGrid
RegionSpec = tuple[Coords, list[int]]

def parse() -> tuple[list[Shape], list[RegionSpec]]:
  shapes = []
  regions = []

  shape = ArrayGrid(N, N)
  y = 0
  for line in data:
    if 'x' in line and ':' in line:
      # Region
      v = ints(line)
      assert len(v) == 8, 'bad region spec'
      regions.append(((v[0], v[1]), v[2:]))
    elif line == '':
      # Shape end.
      shapes.append(shape)
      shape = ArrayGrid(N, N)
      y = 0
    elif ':' not in line:
      # Shape
      for i, ch in enumerate(line):
        if ch == '#':
          shape.setValue(i, y, ch)
      y += 1

  return (shapes, regions)

def applyTransform(shape: Shape, transformations: list[tuple[Coords, Coords]]) -> Shape:
  w, h = shape.getWidth(), shape.getHeight()
  assert w == N and h == N, 'bad shape'
  nshape = ArrayGrid(w, h)
  for (x1, y1), (x2, y2) in transformations:
    nshape.setValue(x2, y2, shape.getValue(x1, y1))
  return nshape

def rotateShapeCW(shape: Shape) -> Shape:
  transformations = [
    ((0, 0), (2, 0)),
    ((1, 0), (2, 1)),
    ((2, 0), (2, 2)),
    ((0, 1), (1, 0)),
    ((1, 1), (1, 1)),
    ((2, 1), (1, 2)),
    ((0, 2), (0, 0)),
    ((1, 2), (0, 1)),
    ((2, 2), (0, 2)),
  ]
  return applyTransform(shape, transformations)

def flipShape(shape: Shape) -> Shape:
  transformations = [
    ((0, 0), (2, 0)),
    ((1, 0), (1, 0)),
    ((2, 0), (0, 0)),
    ((0, 1), (2, 1)),
    ((1, 1), (1, 1)),
    ((2, 1), (0, 1)),
    ((0, 2), (2, 2)),
    ((1, 2), (1, 2)),
    ((2, 2), (0, 2)),
  ]
  return applyTransform(shape, transformations)

CHAR_DISPLAY_COUNTER = 0
def placeShape(region: ArrayGrid, shape: ArrayGrid, start: Coords) -> None:
  global CHAR_DISPLAY_COUNTER
  v = chr(ord('A') + (CHAR_DISPLAY_COUNTER % 26))
  CHAR_DISPLAY_COUNTER += 1
  sx, sy = start
  for x in range(N):
    for y in range(N):
      nx, ny = sx + x, sy + y
      if not shape.hasValue(x, y):
        continue
      assert region.areCoordsWithinBounds(nx, ny) and not region.hasValue(nx, ny), 'bad place checking'
      region.setValue(nx, ny, v)

def canPlaceShape(region: ArrayGrid, shape: ArrayGrid, start: Coords) -> bool:
  sx, sy = start
  for x in range(N):
    for y in range(N):
      nx, ny = sx + x, sy + y
      if not region.areCoordsWithinBounds(nx, ny):
        return False
      if shape.hasValue(x, y) and region.hasValue(nx, ny):
        return False
  return True

def getTransformsToPlace(region: ArrayGrid, transforms: tuple[Shape, ...], start: Coords) -> list[Shape]:
  return [shape for shape in transforms if canPlaceShape(region, shape, start)]

def isRegionLargeEnough(regionSpec: RegionSpec, shapeSizes: dict[int, int]) -> bool:
  regionW, regionH = regionSpec[0]
  totalSize = sum(shapeSizes[i] * regionSpec[1][i] for i in range(len(shapeSizes)))
  return regionW * regionH >= totalSize

def canPlaceAllShapes(
  regionSpec: RegionSpec,
  transformations: dict[int, tuple[Shape, ...]],
  shapeSizes: dict[int, int],
) -> bool:
  if not isRegionLargeEnough(regionSpec, shapeSizes):
    print('region too small')
    return False

  # This puzzle is a load of hot garbage. Uncommenting the line below
  # produces the correct result, and turns the puzzle into something
  # completely trivial. It turns out that the way the input is
  # constructed, the only check necessary is whether the region size is
  # larger than the sum of the blocks in all shapes to place. Actually
  # placing any shapes is not necessary at all.

  # return True

  shapesInOrder = []
  for i, count in enumerate(regionSpec[1]):
    for _ in range(count):
      shapesInOrder.append(i)
  assert len(shapesInOrder) == sum(regionSpec[1]), 'bad shapesInOrderCalculation'

  def placeShapeDfs(region: ArrayGrid, shapeI: int = 0) -> bool:
    if shapeI == len(shapesInOrder):
      print('done:')
      region.print2D({None:'.'})
      return True

    for y in range(region.getHeight() - (N - 1)):
      for x in range(region.getWidth() - (N - 1)):
        shapesToPlace = getTransformsToPlace(region, transformations[shapesInOrder[shapeI]], (x, y))
        for shape in shapesToPlace:
          regionCopy = region.copy()
          placeShape(regionCopy, shape, (x, y))
          if placeShapeDfs(regionCopy, shapeI + 1):
            return True

    return False

  return placeShapeDfs(ArrayGrid(regionSpec[0][0], regionSpec[0][1]))

def part1() -> None:
  shapes, regionSpecs = parse()
  print('data:', len(shapes), len(regionSpecs))
  print('shapes:', len(shapes))
  allTransforms = {}
  shapeSizes = {}
  for i in range(len(shapes)):
    shape = shapes[i]
    shapeSizes[i] = sum(1 if shape.hasValue(x, y) else 0 for x in range(N) for y in range(N))
    assert 5 <= shapeSizes[i] <= 7, 'bad shape size'
    shape.print2D({None: '.'})
    flipped = flipShape(shape)
    transforms = set()
    for _ in range(4):
      transforms.add(shape)
      transforms.add(flipped)
      shape = rotateShapeCW(shape)
      flipped = rotateShapeCW(flipped)
    assert len(transforms) <= 8, 'bad transformations'
    allTransforms[i] = tuple(transforms)
    print('transforms:', len(transforms))
    print('----')

  print('shapeSizes:', shapeSizes)

  ans = 0
  for i, regionSpec in enumerate(regionSpecs):
    print()
    print('*** region:', i, regionSpec[0])
    if canPlaceAllShapes(regionSpec, allTransforms, shapeSizes):
      print('can place')
      ans += 1
  print(ans)

part1()
