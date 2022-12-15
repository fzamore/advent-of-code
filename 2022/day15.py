input = open('day15.txt').read().splitlines()
ROW = 2000000

Coords = tuple[int, int]

def parseInput(input: list[str]) -> list[tuple[Coords, Coords]]:
  result = []
  for line in input:
    sx, sy = map(int, [s.split('=')[1] for s in line.split(':')[0].split(', ')])
    bx, by = map(int, [s.split('=')[1] for s in line.split(':')[1].split(', ')])
    result.append(((sx, sy), (bx, by)))

  return result

# Manhattan distance
def manH(p1: Coords, p2: Coords) -> int:
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

def part1():
  xvalues = set()
  sensors = parseInput(input)
  beaconsSet = set()
  for _, beacon in sensors:
    beaconsSet.add(beacon)
  for sensor, beacon in sensors:
    sx, _ = sensor
    bx, _ = beacon
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

part1()
