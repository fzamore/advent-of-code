from dataclasses import dataclass

input = open('day5.txt').read().split("\n\n")

@dataclass(frozen=True)
class Range:
  dst: int
  src: int
  len: int

@dataclass(frozen=True)
class Map:
  name: str
  ranges: list[Range]

def parseMap(mapStr: str) -> Map:
  lines = mapStr.splitlines()
  name = lines[0].split()[0]
  ranges = []
  for line in lines[1:]:
    dst, src, len = list(map(int, line.split()))
    ranges.append(Range(dst, src, len))
  return Map(name, ranges)

def traceValue(map: Map, value: int) -> int:
  for range in map.ranges:
    if range.src <= value < range.src + range.len:
      return range.dst + value - range.src
  return value

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

part1()
