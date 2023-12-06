from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

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

# Performs an intersection of the two ranges. None represents an empty
# intersection.
def intersectRanges(r1: range, r2: range) -> Optional[range]:
  if r2.start > r1.stop or r1.start > r2.stop:
    return None
  return range(max(r1.start, r2.start), min(r1.stop, r2.stop))

# Subtracts r2 from r1. There are two results, any of which may be empty.
def subtractRanges(r1: range, r2: range) \
  -> tuple[Optional[range], Optional[range]]:
  if r2.stop < r1.start:
    # no overlap
    return (None, r1)
  if r2.start > r1.stop:
    # no overlap
    return (r1, None)
  if r2.start <= r1.start and r2.stop >= r1.stop:
    # r1 entirely contained within r2
    return (None, None)
  if r2.start > r1.start and r2.stop < r1.stop:
    # r2 entirely contained between within r1
    return (range(r1.start, r2.start - 1), range(r2.stop + 1, r1.stop))
  if r2.start <= r1.start:
    return (None, range(r2.stop + 1, r1.stop))
  if r2.stop >= r1.stop:
    return (range(r1.start, r2.start - 1), None)
  else:
    assert False, 'bad range subtraction: %s, %s' % (r1, r2)

# Subtracts multiple ranges from a single range. Only non-empty ranges are
# included in the result. Maximum number of results is 2^(number of
# minuends), due to each individuall subtraction generating up to two
# results (i.e., branching factor of two).
def subtractMultipleRanges(subtrahend: range, minuends: list[range]) \
  -> list[range]:
  subtrahends = defaultdict(list)
  subtrahends[0].append(subtrahend)
  for i in range(len(minuends)):
    for subtra in subtrahends[i]:
      r1, r2 = subtractRanges(subtra, minuends[i])
      if r1 is not None:
        subtrahends[i + 1].append(r1)
      if r2 is not None:
        subtrahends[i + 1]. append(r2)
  return subtrahends[len(minuends)]

# Combines two maps into a single map.
def combineMaps(m1: Map, m2: Map) -> Map:
  allRanges: list[MapRange] = []
  for r1 in m1.ranges:
    rxRanges: list[range] = []
    for r2 in m2.ranges:
      start = r2.start - r1.delta
      end = r2.end - r1.delta

      # intersect (start, end) with r1
      intersection = intersectRanges(
        range(start, end),
        range(r1.start, r1.end),
      )
      if intersection is not None:
        # If there is an intersection, we combine the two deltas.
        rx = range(intersection.start, intersection.stop)
        rxRanges.append(rx)
        allRanges.append(MapRange(rx.start, rx.stop, r1.delta + r2.delta))

    # Subtract each of the intersections from r1.
    for r in rxRanges:
      rx1, rx2 = subtractRanges(range(r1.start, r1.end), r)
      if rx1 is not None:
        allRanges.append(MapRange(rx1.start, rx1.stop, r1.delta))
      if rx2 is not None:
        allRanges.append(MapRange(rx2.start, rx2.stop, r1.delta))
    if len(rxRanges) == 0:
      # if there were no intersections, add the r1 range as is
      allRanges.append(MapRange(r1.start, r1.end, r1.delta))

  # Subtract all ranges so far from all ranges in m2, which preserves the
  # ranges in m2 that are impossible to hit from a range in m1.
  extraM2Ranges = []
  for r2 in m2.ranges:
    results = subtractMultipleRanges(
      range(r2.start, r2.end),
      [range(r.start, r.end) for r in allRanges],
    )
    for result in results:
      extraM2Ranges.append(MapRange(
        result.start,
        result.stop,
        r2.delta,
      ))

  allRanges.extend(extraM2Ranges)
  name = '%s-to-%s' % (
    m1.name.split('-to-')[0],
    m2.name.split('-to-')[1],
  )
  return Map(name, allRanges)

def part1():
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

def part2():
  seedRangeValues = list(map(int, input[0].split(': ')[1].split()))
  assert len(seedRangeValues) % 2 == 0, 'bad seed ranges input'

  seedRanges = []
  for i in range(0, len(seedRangeValues), 2):
    seedRanges.append((seedRangeValues[i], seedRangeValues[i + 1]))
  print(seedRanges)

  maps = [parseMap(x) for x in input[1:]]
  assert len(maps) == 7, 'bad maps input'

  combinedMap = maps[0]
  for i in range(1, len(maps)):
    combinedMap = combineMaps(combinedMap, maps[i])
  print('ranges in combined map:', len(combinedMap.ranges))

  candidates = set()
  for start, length in seedRanges:
    s1, s2 = start, start + length - 1
    for r in combinedMap.ranges:
      rx = intersectRanges(
        range(s1, s2),
        range(r.start, r.end),
      )
      if rx is not None:
        # The intersection exists. Take the lowest seed in the intersection.
        candidates.add(rx.start)
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
