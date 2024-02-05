from collections import Counter, defaultdict

input = open('day6.txt').read().splitlines()

def countTotalOrbits(orbits: dict[str, list[str]], orbit: str, count: int) -> int:
  result = count
  for child in orbits.get(orbit, []):
    result += countTotalOrbits(orbits, child, count + 1)
  return result

def part1() -> None:
  orbits = defaultdict(list)
  for line in input:
    orbitee, orbiter = line.split(')')
    orbits[orbitee].append(orbiter)
  print(countTotalOrbits(orbits, 'COM', 0))

part1()
