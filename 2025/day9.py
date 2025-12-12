from common.ints import ints
from itertools import combinations
from common.sparsegrid import SparseGrid

data = open('day9.txt').read().splitlines()

Coords = tuple[int, int]
Segment = tuple[Coords, Coords]

# Checks whether the given point is inside the region. We shoot a "beam"
# in each of the four cardinal direction from the point, and if the beam
# exits the region (i.e., it escapes the bounding rectangle for the entire
# region) without intersecting the region's perimeter, we know the point
# is not within the region.
def isInsideRegion(grid: SparseGrid, coords: Coords) -> bool:
  if grid.hasValue(coords):
    return True

  x, y = coords
  (xmin, ymin), (xmax, ymax) = grid.getMinCoords(), grid.getMaxCoords()
  deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
  for dx, dy in deltas:
    nx, ny = x + dx, y + dy
    hitPerimeter = False
    while xmin <= nx <= xmax and ymin <= ny <= ymax:
      if grid.hasValue((nx, ny)):
        # We have hit the perimeter. The point is in the region in this direction.
        hitPerimeter = True
        break
      nx += dx
      ny += dy

    if not hitPerimeter:
      # The beam escaped. This point is not within the region.
      return False

  return True

# Returns whether the two segments are parallel.
def areSegmentsParallel(s1: Segment, s2: Segment) -> bool:
  (c1, c2), (c3, c4) = s1, s2
  (x1, y1), (x2, y2) = c1, c2
  (x3, y3), (x4, y4) = c3, c4
  assert (x1 == x2 or y1 == y2) and (x3 == x4 or y3 == y4), 'bad segments'

  return (x1 == x2 and x3 == x4) or (y1 == y2 and y3 == y4)

# Returns whether the two segments completely cross. Parallel segments are
# not considered crossing.
def doSegmentsCross(s1: Segment, s2: Segment) -> bool:
  (c1, c2), (c3, c4) = s1, s2
  (x1, y1), (x2, y2) = c1, c2
  (x3, y3), (x4, y4) = c3, c4
  assert (x1 == x2 or y1 == y2) and (x3 == x4 or y3 == y4), 'bad segments'

  if areSegmentsParallel(s1, s2):
    return False

  if x1 == x2:
    assert x3 != x4 and y3 == y4, 'bad parallel checking'
    return min(x3, x4) < x1 and max(x3, x4) > x1 and min(y1, y2) < y3 and max(y1, y2) > y3
  else:
    assert y1 == y2, 'bad segment'
    assert y3 != y4 and x3 == x4, 'bad parallel checking'
    return min(y3, y4) < y1 and max(y3, y4) > y1 and min(x1, x2) < x3 and max(x1, x2) > x3

def part1() -> None:
  coords = [ints(line) for line in data]
  print('coords:', len(coords))

  mx = -1
  for c1, c2 in combinations(coords, 2):
    (x1, y1), (x2, y2) = c1, c2
    area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
    mx = max(mx, area)
  print(mx)

def part2() -> None:
  # This algorithm is slow, but it produces the correct answer (at least
  # for my input). A box is within the region if a/ none of its four sides
  # cross a region boundary and b/ all four corners of the box are within
  # the region. In my implementation, checking whether a point is within
  # the region is slow, so I only do this check if none of the box's
  # segments cross a region boundary.

  print()
  print('***** SHOULD COMPLETE IN <10s WITH pypy. OVER 30s WITH python *****')
  print()

  coords = []
  for line in data:
    v = tuple(ints(line))
    assert len(v) == 2, 'bad input line'
    coords.append(v)
  n = len(coords)
  print('coords:', n)

  # Computing list of segments.
  segments = []
  for i in range(n):
    if i < n - 1:
      segments.append((coords[i], coords[i + 1]))
  segments.append((coords[n - 1], coords[0]))
  print('segments:', len(segments))
  assert len(segments) == len(coords), 'bad segment computation'

  # Adding all segments to the grid.
  grid = SparseGrid(2)
  for (x1, y1), (x2, y2) in segments:
    assert x1 == x2 or y1 == y2, 'bad segment'
    if x1 == x2:
      for y in range(min(y1, y2), max(y1, y2) + 1):
        grid.setValue((x1, y), 'X')
    else:
      for x in range(min(x1, x2), max(x1, x2) + 1):
        grid.setValue((x, y1), 'X')

  print('min/max:', grid.getMinCoords(), grid.getMaxCoords())
  (xmin, ymin), (xmax, ymax) = grid.getMinCoords(), grid.getMaxCoords()
  print('bounding rect size:', (xmax - xmin + 1) * (ymax - ymin) + 1)

  # Assembling all potential boxes in decreasing-area order.
  boxes = []
  for c1, c2 in combinations(coords, 2):
    (x1, y1), (x2, y2) = c1, c2
    area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
    boxes.append((area, c1, c2))
  print('boxes:', len(boxes))

  print('sorting...')
  boxes.sort(reverse=True)
  print('done')

  print('checking...')
  for (area, c1, c2) in boxes:
    (x1, y1), (x2, y2) = c1, c2
    c3, c4 = (x1, y2), (x2, y1)

    isValidBox = True
    for s in ((c1, c3), (c3, c2), (c2, c4), (c4, c1)):
      for seg in segments:
        if doSegmentsCross(s, seg):
          # This box crosses the region. It's invalid.
          isValidBox = False
          break

    if isValidBox:
      if isInsideRegion(grid, c3) and isInsideRegion(grid, c4):
        # Both alternate corners are inside the region. We've found our box.
        print('done:', area, c1, c2)
        print(area)
        return

  assert False, 'did not find answer'

part2()
