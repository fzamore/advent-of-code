from more_itertools import pairwise

input = open('day15.txt').read().splitlines()
ROW = 2000000
MAX = 4000000
#MAX = 20

Coords = tuple
Segment = tuple

def parseInput(input: list) -> list:
  result = []
  for line in input:
    sx, sy = map(int, [s.split('=')[1] for s in line.split(':')[0].split(', ')])
    bx, by = map(int, [s.split('=')[1] for s in line.split(':')[1].split(', ')])
    result.append(((sx, sy), (bx, by)))

  return result

# Manhattan distance
def manH(p1: Coords, p2: Coords) -> int:
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

# Adds the given segment to the list of segments, and does any merging or
# updating existing segments as needed.
def addSegmentToLine(segments: list, segment: Segment) -> None:
  x1, x2 = segment
  x1 = max(x1, 0)
  x2 = min(x2, MAX - 1)
  assert x1 <= x2, 'bad segment: %d, %d' % (segment[0], segment[1])

  for i in range(len(segments)):
    p1, p2 = segments[i]
    if x2 < p1:
      # The new segment is located to the left of the existing segment and
      # does not overlap. Insert the new segment before the existing
      # segment as-is.
      segments.insert(i, (x1, x2))
      return

    if x1 > p2:
      # The new segment is located to the right of the existing segment
      # and does not overlap. Keep going.
      continue

    # At this point, we have overlap with segment i. Compute the
    # overlapping region.

    if x1 >= p1 and x2 <= p2:
      # The existing segment completely contains the new segment. No
      # update needed.
      return

    # Search forward through remaining segments any that overlap with the
    # new segment.
    overlapping = 0
    j = i + 1
    while j < len(segments) and x2 >= segments[j][0]:
      overlapping += 1
      j += 1

    if overlapping == 0:
      # The new segment does not overlap with a second segment. Update the
      # start position of the existing segment.
      assert x1 <= p2
      segments[i] = (min(x1, p1), max(x2, p2))
      return

    # The existing segment overlaps parts of at least segments. Delete all
    # but the first, and update the first one.
    assert j > i
    segments[i] = (min(x1, p1), max(x2, segments[i + overlapping][1]))
    for _ in range(overlapping):
      segments.pop(i + 1)
    return

  # At this point, we didn't find an overlapping segment. Insert the new
  # segment at the end of the list.
  segments.append((x1, x2))

def part1():
  sensors = parseInput(input)
  beaconsSet = set()
  for _, beacon in sensors:
    beaconsSet.add(beacon)
  xvalues = set()
  for sensor, beacon in sensors:
    sx, _ = sensor
    dx = 0
    bdist = manH(sensor, beacon)
    print('testing sensor', sensor, bdist)
    # Find all points along the line that are at least as close as this
    # sensor's beacon. Start on the line at the sensor's x-coordinate and
    # move outward in both directions in lockstep.
    while manH(sensor, (sx + dx, ROW)) <= bdist:
      # As long as the test point is not further than the sensor's beacon,
      # add the test point and the point an equal x-distance to the left
      # as well (since both points have the same Manhattan distance from
      # the sensor).
      for nx in [sx + dx, sx - dx]:
        if (nx, ROW) not in beaconsSet:
          # Add the point as an "impossible point" if there isn't already
          # a beacon there.
          xvalues.add(nx)
      dx += 1

  print(len(xvalues))

def part2():
  sensors = parseInput(input)
  print('number of sensors:', len(sensors))

  # Algorithm: Each sensor describes a diamond-shaped pattern, centered at
  # the sensor, in which another beacon cannot exist. The horizontal and
  # vertical "radius" of the pattern is determined by the Manhattan
  # distance to its beacon. The goal is to compute the overlap of each
  # sensor's diamond. There will be exactly one coordinate within the
  # (0,0) -> (MAX-1, MAX-1) square that isn't in any region, which is the
  # point we care about.
  #
  # To find the point, maintain a MAX-length array of lists of line
  # segments representing each row in the region (a line segment is a
  # (start, end) tuple). We iterate top-to-bottom over each sensor's
  # diamond, and for each row in the diamond, we compute its line segment,
  # and then place it at the appropriate place in the corresponding row's
  # list of segments. This may involve merging segments or embiggening an
  # existing segment.
  #
  # After this process, each list in the data structure should contain
  # enough segments to span the entire line (usuallly just a single (0,
  # MAX-1) segment), *except for one*, which contains the point we're
  # looking for.

  # Each element in this array is a list of non-overlapping line segments
  # representing where beacons cannot be placed. Each list is sorted by
  # start coordinate.
  allSegments = [[] for _ in range(MAX)]

  for sensor, beacon in sensors:
    sx, sy = sensor
    dist = manH(sensor, beacon)
    print('processing sensor:', sensor, dist)
    # iterate from top-to-bottom for a sensor's range
    for y in range(max(sy - dist, 0), min(sy + dist, MAX - 1) + 1):
      numpoints = 2 * (dist - abs(sy - y)) + 1
      assert numpoints % 2 == 1, 'bad numpoints: %s' % numpoints
      segment = (sx - (numpoints // 2), sx + (numpoints // 2))
      if segment[0] > MAX - 1 or segment[1] < 0:
        # This segment does not intersect the area we care about. Skip.
        continue

      addSegmentToLine(allSegments[y], segment)

  # We've computed the overlap. Find the point that isn't covered.
  for y in range(MAX):
    segments = allSegments[y]
    if len(segments) == 1:
      p1, p2 = segments[0]
      if p1 != 0 or p2 != MAX - 1:
        print('found row', y)
        break
    for seg1, seg2 in pairwise(segments):
      if seg2[0] - seg1[1] != 1:
        # There is a gap between segments. Bingo.
        print(segments)
        x = seg1[1] + 1
        print('found point:', x, y)
        print(4000000 * x + y)
      break

part2()
