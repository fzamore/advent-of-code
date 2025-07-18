from common.ints import ints
from collections import defaultdict

data = open('day14.txt').read().splitlines()

Reindeer = dict[str, tuple[int, int, int]]

def parseInput() -> Reindeer:
  reindeer = {}
  for line in data:
    vel, time, rest = ints(line)
    reindeer[line.split()[0]] = vel, time, rest
  return reindeer

def dist(reindeer: Reindeer, name: str, seconds: int) -> int:
  vel, time, rest = reindeer[name]
  m = time + rest
  return vel * (time * (seconds // m) + min(time, seconds % m))

def part1() -> None:
  reindeer = parseInput()
  print('input:', len(reindeer))
  n = 2503
  print(max(d for d in (dist(reindeer, name, n) for name in reindeer)))

def part2() -> None:
  reindeer = parseInput()
  n = 2503
  points: dict[str, int] = defaultdict(int)
  for i in range(1, n + 1):
    distances = dict([(name, dist(reindeer, name, i)) for name in reindeer])
    maxd = max(distances.values())
    for name in reindeer:
      if distances[name] == maxd:
        points[name] += 1
  print('result:', points)
  print(max(points.values()))

part2()
