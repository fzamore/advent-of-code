from collections import defaultdict
from typing import Callable

data = open('day9.txt').read().splitlines()

Graph = defaultdict[tuple[str, str], int]

def parseInput() -> tuple[set[str], Graph]:
  graph = defaultdict(int)
  cities = set()
  for s in data:
    v = s.split()
    assert len(v) == 5, 'bad data'
    cities.add(v[0])
    cities.add(v[2])
    graph[v[0], v[2]] = int(v[4])
    graph[v[2], v[0]] = int(v[4])
  return cities, graph

def optimize(
  graph: Graph,
  optimizeFn: Callable[[list[int]], int],
  remainingCities: set[str],
  distance: int = 0,
  currentCity: str = '',
) -> int:
  if len(remainingCities) == 1:
    return distance

  # Visit the current city.
  r = remainingCities.difference({currentCity})

  # Pick the best distance among all remaining cities.
  return optimizeFn(
    [optimize(graph, optimizeFn, r, distance + graph[currentCity, c], c) for c in r]
  )

def part1() -> None:
  print('lines:', len(data))
  cities, graph = parseInput()
  print('cities:', len(cities))

  print(optimize(graph, min, cities))

def part2() -> None:
  print('lines:', len(data))
  cities, graph = parseInput()
  print('cities:', len(cities))

  print(optimize(graph, max, cities))

part2()
