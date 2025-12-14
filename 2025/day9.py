from common.ints import ints
from itertools import combinations
from common.sparsegrid import SparseGrid

data = open('day9.txt').read().splitlines()

Coords = tuple[int, int]
Segment = tuple[Coords, Coords]

# Checks whether the given point is inside the region by raycasting to the
# left. This is implemented by counting all vertical edges to the left of
# the point and determining which ones intersect with the y coordinate of
# the point (i.e., a ray cast to the left would hit it). If there are an
# even number, the point is outside the region, and if odd, it's inside.
def isPointInsideRegion(grid: SparseGrid, vsegments: list[Segment], coords: Coords) -> bool:
  if grid.hasValue(coords):
    return True

  x, y = coords
  parity = 0
  for (startx, starty), (endx, endy) in vsegments:
    assert startx == endx, 'not vertical segment'
    if startx > x:
      # This edge is to the right of the point. Ignore it.
      continue

    # Add a delta to the y value so we're comparing "between" valid y
    # coordinates and are thus guaranteed to never hit a horizontal line.
    # This can be tricky when testing a point at the very bottom of the
    # region (since adding the delta pushes the point below the boundary),
    # but those cases are handled by the hasValue check at the beginning
    # (i.e., if a point is at the very bottom, it is in the region iff it
    # is on the perimeter).
    if min(starty, endy) <= y + 0.5 <= max(starty, endy):
      parity += 1

  return parity % 2 == 1

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
  print('***** SHOULD COMPLETE IN <2s WITH pypy. OVER 20s WITH python *****')
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
  vsegments = []
  for i in range(n):
    if i < n - 1:
      segments.append((coords[i], coords[i + 1]))
      seg = segments[-1]
      if seg[0][0] == seg[1][0]:
        vsegments.append(seg)
  segments.append((coords[n - 1], coords[0]))
  seg = segments[-1]
  if seg[0][0] == seg[1][0]:
    vsegments.append(seg)
  print('segments:', len(segments))
  print('vsegments:', len(vsegments))
  assert len(segments) == len(coords), 'bad segment computation'
  assert len(segments) % 2 == 0 and len(segments) // 2 == len(vsegments), 'bad vsegments computations'

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
      if isPointInsideRegion(grid, vsegments, c3) and isPointInsideRegion(grid, vsegments, c4):
        # Both alternate corners are inside the region. We've found our box.
        print('done:', area, c1, c2)
        print(area)
        return

  assert False, 'did not find answer'

part2()
