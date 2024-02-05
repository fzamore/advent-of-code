from collections import defaultdict
from typing import Optional

input = open('day6.txt').read().splitlines()

def countTotalOrbits(
  orbits: dict[str, list[str]],
  orbit: str,
  count: int = 0,
) -> int:
  result = count
  for child in orbits[orbit]:
    result += countTotalOrbits(orbits, child, count + 1)
  return result

def distToNode(
  orbits: dict[str, list[str]],
  src: str,
  dst: str,
  count: int = 0,
) -> Optional[int]:
  if src == dst:
    return count

  for child in orbits[src]:
    result = distToNode(orbits, child, dst, count + 1)
    if result is not None:
      return result

  return None

def part1() -> None:
  orbits = defaultdict(list)
  for line in input:
    orbitee, orbiter = line.split(')')
    orbits[orbitee].append(orbiter)
  print(countTotalOrbits(orbits, 'COM'))

def part2() -> None:
  orbits = defaultdict(list)
  parents = {}
  for line in input:
    orbitee, orbiter = line.split(')')
    orbits[orbitee].append(orbiter)
    parents[orbiter] = orbitee

  src = 'YOU'
  dst = 'SAN'

  distToSrc = 0
  while (distToDst := distToNode(orbits, src, dst)) is None:
    src = parents[src]
    distToSrc += 1
  print('found dist:', src, distToSrc, distToDst)
  # Subtract 2 to discount YOU and SAN
  print(distToSrc + distToDst - 2)

part2()
