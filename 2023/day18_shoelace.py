from collections import namedtuple

input = open('day18.txt').read().splitlines()

Segment = namedtuple('Segment', ['start', 'delta', 'length'])

# Returns the area of the polygon enclosed by the given segments, by
# implementing the Shoelace Formula:
# https://en.wikipedia.org/wiki/Shoelace_formula.
#
# The Shoelace Formula is designed for traditional coordinates, which
# appear at the intersections of grid squares. Our coordinates are the
# squares themselves, however, so using the formula as-is will produce an
# area as if the polygon's border instead connected the *midpoint* of each
# square. Thus, this result includes a number of squares cut in half, and
# squares cut in quarters. We need to add to the result the remainder of
# each of these partial squares. Each non-corner border point is a half
# square. Each corner point is either a 1/4-square (right turn) or a
# 3/4-square (left turn). This function assumes that segments are given in
# clockwise order (the code does not ensure this; it happens to work out
# for the input).
def shoelaceAreaIncludingBorder(segments: list[Segment]) -> int:
  rightTurns = {
    (1, 0): (0, 1),
    (0, 1): (-1, 0),
    (-1, 0): (0, -1),
    (0, -1): (1, 0),
  }

  innerValue, halfPoints, oneQuarterPoints, threeQuarterPoints = 0, 0, 0, 0
  for i, seg in enumerate(segments):
    (x1, y1), (dx, dy), length = seg
    assert length > 0, 'cannot have negative lengths'

    x2, y2 = x1 + dx * length, y1 + dy * length

    # Shoelace.
    innerValue += (x1 * y2) - (x2 * y1)

    # All points oon the segment are half points except the corners.
    halfPoints += length - 1

    nextDelta = segments[(i + 1) % len(segments)].delta
    assert (dx, dy) != nextDelta, 'two consecutive deltas equal'
    if nextDelta == rightTurns[(dx, dy)]:
      # Right turns enclose a one-quarter point.
      oneQuarterPoints += 1
    else:
      # Left turns enclose a three-quarter point.
      threeQuarterPoints += 1

  print('innerValue:', innerValue // 2)
  print('halfPoints:', halfPoints)
  print('1/4 points:', oneQuarterPoints)
  print('3/4 points:', threeQuarterPoints)
  assert innerValue % 2 == 0, 'bad innerValue'
  assert halfPoints % 2 == 0, 'bad halfPoints'
  assert (3 * oneQuarterPoints + threeQuarterPoints) % 4 == 0, 'bad quarterPoints'
  assert oneQuarterPoints + threeQuarterPoints == len(segments), 'bad math'

  # The quarter points are included as follows:
  #  (3/4) * oneQuarterPoints + (1/4) * threeQuarterPoints
  return \
    innerValue // 2 + \
    halfPoints // 2 + \
    (3 * oneQuarterPoints + threeQuarterPoints) // 4

def part1() -> None:
  deltas = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
  }

  x, y = 0, 0
  segments = []
  for line in input:
    values = line.split()
    dir = values[0]
    qty = int(values[1])
    dx, dy = deltas[dir]

    segments.append(Segment((x, y), (dx, dy), qty))

    x += dx * qty
    y += dy * qty

  print('segments:', len(segments))

  print(shoelaceAreaIncludingBorder(segments))

def part2() -> None:
  deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  segments = []
  x, y = 0, 0
  for line in input:
    values = line.split()

    dx, dy = deltas[int(values[2][-2])]
    qty = int(values[2][2:-2], 16)

    segments.append(Segment((x, y), (dx, dy), qty))

    x += qty * dx
    y += qty * dy

  print('segments:', len(segments))
  print(shoelaceAreaIncludingBorder(segments))

part2()
