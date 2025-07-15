from itertools import permutations
from collections import defaultdict

data = open('day13.txt').read().splitlines()

Graph = defaultdict[tuple[str, str], int]

def parseInput() -> Graph:
  graph = defaultdict(int)
  for line in data:
    v = line.split()
    assert len(v) == 11, 'bad input line'
    p1 = v[0]
    p2 = v[-1][:-1]
    val = int(v[3])
    if 'lose' in v:
      val = -val
    graph[p1, p2] = val
  return graph

def calc(graph: Graph, circle: tuple[str, ...]) -> int:
  score = 0
  for i in range(len(circle)):
    j = (i + 1) % len(circle)
    score += graph[circle[i], circle[j]]
    score += graph[circle[j], circle[i]]
  return score

def part1() -> None:
  print('lines:', len(data))
  d = parseInput()
  names = set([k[0] for k in d])
  print('names:', len(names), names)

  print(max(calc(d, c) for c in permutations(names)))

def part2() -> None:
  print('lines:', len(data))
  d = parseInput()
  names = set([k[0] for k in d])
  names.add('me')
  print('names:', len(names), names)

  print(max(calc(d, c) for c in permutations(names)))

part2()
