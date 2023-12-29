from decimal import Decimal
from itertools import combinations
from typing import Iterator, Optional

input = open('day24.txt').read().splitlines()

Coords = tuple[Decimal, Decimal, Decimal]
Velocities = tuple[Decimal, Decimal, Decimal]
XYIntersection = tuple[Decimal, Decimal]

Stone = tuple[Coords, Velocities]

def parseInput() -> list[Stone]:
  result = []
  for line in input:
    v = line.split( ' @ ')
    # Use Decimial because it's 2023 and computers still can't do floating
    # point correctly.
    x, y, z = map(Decimal, v[0].split(', '))
    dx, dy, dz = map(Decimal, v[1].split(', '))
    assert dx != 0 and dy != 0 and dz != 0, 'no zeroes allowed in velocity'
    result.append(((x, y, z), (dx, dy, dz)))
  return result

# Returns the x-y intersection of the two given stones when projected onto
# a 2D plane (i.e., ignoring the z-coordinate), or None, if they're
# parallel.
def findXYIntersection(s1: Stone, s2: Stone) -> Optional[XYIntersection]:
  (x1, y1, _), (dx1, dy1, _) = s1
  (x2, y2, _), (dx2, dy2, _) = s2

  # Convert everything into "y = mx + b" form.

  m1 = Decimal('Infinity') if dx1 == 0 else dy1 / dx1
  m2 = Decimal('Infinity') if dx2 == 0 else dy2 / dx2

  if m1 == m2:
    # Slopes are equal; stones are parallel.
    return None

  assert dx1 != 0 or dx2 != 0, 'bad parallel checking'

  if dx1 != 0:
    b1 = y1 - x1 * dy1 / dx1
  if dx2 != 0:
    b2 = y2 - x2 * dy2 / dx2

  if dx1 == 0:
    return x1, x1 * m2 + b2

  if dx2 == 0:
    return x2, x2 * m1 + b1

  xi = (b2 - b1) / (dy1 / dx1 - dy2 / dx2)
  yi = xi * dy1 / dx1 + b1
  # Quantize because computers still can't do floating point. Without
  # this, using == on Decimal won't work properly.
  return (xi.quantize(Decimal('0.001')),yi.quantize(Decimal('0.001')))

# Returns whether the given x-y intersection is in the past for the given
# stone.
def isIntersectionInPast(s: Stone, ix: XYIntersection) -> bool:
  (x, y, _), (dx, dy, _) = s
  xi, yi = ix
  if dx != 0 and (xi - x) / dx < 0:
    return True

  if dy != 0 and (yi - y) / dy < 0:
    return True

  # This may return an incorrect result if dx and dy are both zero, but it
  # still yields the correct answer.
  return False

# Returns the x-y intersection of the two given stones when projected onto
# a 2D plane (i.e., ignoring the z-coordinate) if the intersection occurs
# in the future (i.e., if the intersection occurs before t == 0, this
# function returns None).
def findXYIntersectionInFuture(s1: Stone, s2: Stone) \
  -> Optional[XYIntersection]:
  intersection = findXYIntersection(s1, s2)
  if intersection is None:
    return None

  if isIntersectionInPast(s1, intersection) or \
    isIntersectionInPast(s2, intersection):
    return None

  return intersection

# Returns the position of a stone at time t.
def computePosition(s: Stone, t: Decimal) -> Coords:
  (x, y, z), (vx, vy, vz) = s
  return (
    x + vx * t,
    y + vy * t,
    z + vz * t,
  )

# Returns the time at which the given stone reaches the given x-y
# position.
def computeTimeinXY(s: Stone, xy: tuple[Decimal, Decimal]) -> Decimal:
  (x, y, _), (vx, vy, _) = s
  assert vy != 0 or vx != 0, 'both vx and vy cannot be 0'

  if vx != 0:
    return (xy[0] - x) / vx
  return (xy[0] - y) / vy

# Returns all x-y coordinates that are the given manhattan distance from
# the origin.
def allXYCoordsForManhattanDistance(n: int) -> Iterator[tuple[int, int]]:
  for x in range(n + 1):
    y = n - x
    if x == 0 or y == 0:
      # Skip zeroes for simplicity. We assume the new stone doesn't
      # include a zero velocity component.
      continue
    for dx, dy in [(-1, 1), (-1, -1), (1, -1), (1, 1)]:
      ax = x * dx
      ay = y * dy
      assert abs(ax) + abs(ay) == n, 'bad manhattan distance'
      yield ax, ay

# "Adjusts" the given stone's x- and y-velocities by subtracting the given
# amounts.
def adjustStoneXYVelocities(s: Stone, vxd: int, vyd: int) -> Stone:
  p, (vx, vy, vz) = s
  return (p, (vx - vxd, vy - vyd, vz))

def part1() -> None:
  stones = parseInput()
  print('stones:', len(stones))

  minPos = 200000000000000
  maxPos = 400000000000000

  valid = []
  for s1, s2 in combinations(stones, 2):
    intersection = findXYIntersectionInFuture(s1, s2)
    if intersection is None:
      continue

    xi, yi = intersection
    if not minPos <= xi <= maxPos or not minPos <= yi <= maxPos:
      continue

    valid.append((s1, s2, (xi, yi)))

  print()
  print(len(valid))

def part2() -> None:
  allStones = parseInput()
  print('input stones:', len(allStones))

  # I stole this algorithm from Reddit.
  #
  # Treat the new stone as if it is not moving by "adjusting" all existing
  # stones by the new stone's x- and y-velocities (by subtraction:
  # v_existingStone - v_newStone). Then, the problem becomes finding the
  # single point at which all the adjusted stones intersect. We find the
  # xy intersection (i.e., ignore z) for simplicity. Since the input
  # velocity values are relatively small (i.e., less than 1000), we can
  # brute force checking them, starting from zero and radiating outward in
  # both positive and negative directions. (Note that the positions and
  # time values are both very large, so these cannot easily be brute
  # forced).
  #
  # So, for each brute-forced velocity pair, intersect the first stone
  # with all other stones, and if they all share the same xy-intersection
  # point, then the x- and y-velocities of the new stone are the ones
  # we're currently checking. The x and y initial positions of the new
  # stone are the intersection point. Finding the z-velocity and z
  # position is algebra.
  #
  # In theory, this algorithm could yield a result that matches in xy, but
  # doesn't match in z, so I should verify that all stones intersect in
  # the z-coordinate as well, but the xy match was the correct answer, so
  # I didn't bother to do that extra verification.

  s1 = allStones[0]
  # Start at manhattan distance 2 and "radiate" outward until we found a solution.
  manhDist = 2
  while True:
    for vxi, vyi in allXYCoordsForManhattanDistance(manhDist):
      intersectionCount = 0
      totalIntersection = None
      as1 = adjustStoneXYVelocities(s1, vxi, vyi)
      for s2 in allStones[1:]:
        as2 = adjustStoneXYVelocities(s2, vxi, vyi)
        intersection = findXYIntersectionInFuture(as1, as2)
        if intersection is None:
          # There was no future intersection.
          break

        if totalIntersection is None:
          # Store this intesection if we haven't seen one yet.
          totalIntersection = intersection
        assert totalIntersection is not None, 'bad intersect logic'

        if totalIntersection != intersection:
          # The intersections do not match. Skip.
          break

        # At this point, we have a valid intersection.
        intersectionCount += 1

      if intersectionCount == len(allStones) - 1:
        # Every stone intersected at the same xy point, which is the
        # starting point of the new stone.
        assert totalIntersection is not None, 'should have found intersection'
        print('found adjusted xy intersection:', vxi, vyi, totalIntersection)

        # The time at which the first adjusted stone hits the intersection
        # point.
        t1 = computeTimeinXY(as1, totalIntersection)
        print('intersection t1:', t1)

        # The time at which the second adjusted stone hits the intersection
        # point.
        as2 = adjustStoneXYVelocities(allStones[1], vxi, vyi)
        t2 = computeTimeinXY(as2, totalIntersection)
        print('intersection t2:', t2)

        assert t1 != t2, 'bad time math'

        # The non-adjusted intersection point, computed from the first
        # stone (non-adjusted).
        pos1 = computePosition(s1, t1)
        print('non-adjusted intersection 1:', pos1)

        # The non-adjusted intersection point, computed from the second
        # stone (non-adjusted).
        pos2 = computePosition(allStones[1], t2)
        print('non-adjusted intersection 2:', pos2)

        # The z-velocity of the new stone is the delta between z-values of
        # the two intersection points of the first two stones (now that
        # the intersection points are non-adjusted, these points will be
        # different) divided by the difference in time between the two
        # intersections.
        assert int(pos2[2] - pos1[2]) % int(t2 - t1) == 0, \
          'vzi should be integer'
        vzi = (pos2[2] - pos1[2]) // (t2 - t1)
        print('vzi:', vzi)

        # Compute the initial z position based on the z-velocity and first
        # intersection position/time.
        z = pos1[2] - vzi * t1
        print('z:', z)

        print(round(totalIntersection[0] + totalIntersection[1] + z))
        return

    # Increase manhattan distance to radiate outward.
    manhDist += 1

part2()
