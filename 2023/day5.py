from dataclasses import dataclass
from typing import Optional
from common.ranges import intersectRanges, subtractMultipleRanges

input = open('day5.txt').read().split("\n\n")

# All ranges (both MapRange and range) are inclusive.

@dataclass(frozen=True)
class MapRange:
  start: int
  end: int # inclusive
  delta: int # the amount to add to the seed to get the destination

@dataclass(frozen=True)
class Map:
  name: str
  ranges: list[MapRange]

def parseMap(mapStr: str) -> Map:
  lines = mapStr.splitlines()
  name = lines[0].split()[0]
  ranges = []
  for line in lines[1:]:
    dst, src, len = list(map(int, line.split()))
    ranges.append(MapRange(src, src + len - 1, dst - src))
  return Map(name, ranges)

# Traces a single seed value through a single map.
def traceValue(map: Map, value: int) -> int:
  for range in map.ranges:
    if range.start <= value <= range.end:
      return value + range.delta
  return value

# Combines two maps into a single map.
def combineMaps(m1: Map, m2: Map) -> Map:
  intersectionRanges: list[MapRange] = []
  # Compute all ranges that can be hit from a range in m1 then a range in m2.
  for r1 in m1.ranges:
    for r2 in m2.ranges:
      # Subtract deltas to go backwards from m2 to m1.
      start = r2.start - r1.delta
      end = r2.end - r1.delta

      # intersect (start, end) with r1
      intersection = intersectRanges((start, end), (r1.start, r1.end))
      if intersection is not None:
        # If there is an intersection, we add the two deltas, because they
        # will get applied in sequence.
        intersectionRanges.append(
          MapRange(intersection[0], intersection[1], r1.delta + r2.delta)
        )

  # Subtract the intersection ranges from all ranges in m1 and m2, and add
  # the resuts of the subtraction. This preserves values that will hit
  # exacty one range in m1 or m2.
  existingRanges = []
  for r1 in m1.ranges:
    results = subtractMultipleRanges(
      (r1.start, r1.end),
      [(r.start, r.end) for r in intersectionRanges],
    )
    for start, end in results:
      existingRanges.append(MapRange(start, end, r1.delta))

  for r2 in m2.ranges:
    results = subtractMultipleRanges(
      (r2.start, r2.end),
      [(r.start, r.end) for r in intersectionRanges],
    )
    for start, end in results:
      existingRanges.append(MapRange(start, end, r2.delta))

  intersectionRanges.extend(existingRanges)
  name = '%s-to-%s' % (
    m1.name.split('-to-')[0],
    m2.name.split('-to-')[1],
  )
  return Map(name, intersectionRanges)

def part1() -> None:
  seeds = list(map(int, input[0].split(': ')[1].split()))
  print('seeds:', seeds)
  print(len(seeds))
  print()

  maps = [parseMap(x) for x in input[1:]]
  assert len(maps) == 7, 'bad maps input'

  locations = []
  for seed in seeds:
    value = seed
    for m in maps:
      value = traceValue(m, value)
    print(seed, value)
    locations.append(value)

  print(min(locations))

def part2() -> None:
  seedRangeValues = list(map(int, input[0].split(': ')[1].split()))
  assert len(seedRangeValues) % 2 == 0, 'bad seed ranges input'

  seedRanges = []
  for i in range(0, len(seedRangeValues), 2):
    seedRanges.append((seedRangeValues[i], seedRangeValues[i + 1]))
  print(seedRanges)

  maps = [parseMap(x) for x in input[1:]]
  assert len(maps) == 7, 'bad maps input'

  # Combine all of the maps.
  combinedMap = maps[0]
  for i in range(1, len(maps)):
    combinedMap = combineMaps(combinedMap, maps[i])
  print('ranges in combined map:', len(combinedMap.ranges))

  # Compute a list of seed candidates for lowest location.
  candidates = set()
  for start, length in seedRanges:
    s1, s2 = start, start + length - 1
    for r in combinedMap.ranges:
      rx = intersectRanges((s1, s2), (r.start, r.end))
      if rx is not None:
        # The intersection exists. Take the lowest seed in the intersection.
        candidates.add(rx[0])
      else:
        # If this seed range didn't match any map ranges, then there is a
        # 1:1 mapping for everything in this range. Take the lowest value.
        candidates.add(s1)

  mappedValues = {}
  for candidate in candidates:
    mappedValues[candidate] = traceValue(combinedMap, candidate)

  print()
  print(min(mappedValues.values()))

part2()
