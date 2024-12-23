from collections import defaultdict
from itertools import combinations

input = open('day23.txt').read().splitlines()

Graph = dict[str, set[str]]

def parseInput() -> Graph:
  graph = defaultdict(set)
  for line in input:
    n1, n2 = line.split('-')
    graph[n1].add(n2)
    graph[n2].add(n1)

  print('nodes:', len(graph))
  return graph

# Returns whether the given node is connected with every node in the given set.
def isFullyConnected(graph: Graph, s: set[str], node: str) -> bool:
  assert node not in s, 'node already in set'
  for n in s:
    if node not in graph[n]:
      return False
  return True

def buildMaxSetFromNode(graph: Graph, node: str) -> set[str]:
  s = {node}
  for n in graph:
    if n not in s and isFullyConnected(graph, s, n):
      s.add(n)
  return s

def part1() -> None:
  graph = parseInput()

  triples = set()
  for n1, n2 in combinations(graph, 2):
    if n1 not in graph[n2]:
      continue
    assert n2 in graph[n1], 'graph not bidirectional'

    for n3 in graph[n2]:
      if n3 in graph[n1]:
        triples.add(tuple(sorted([n1, n2, n3])))

  print('triples:', len(triples))
  ans = sum(1 for t in triples if any(n[0] == 't' for n in t))
  print(ans)

def part2() -> None:
  graph = parseInput()
  best = 0
  bestSet = None
  for node in graph:
    s = buildMaxSetFromNode(graph, node)
    if len(s) > best:
      best = len(s)
      bestSet = s

  assert bestSet is not None, 'did not find answer'
  print('best:', best, bestSet)
  print(','.join(sorted(bestSet)))

part2()
