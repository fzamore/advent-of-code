input = open('day12.txt').read().splitlines()

Node = int
Graph = dict[Node, list[Node]]

def parseInput() -> Graph:
  graph = {}
  for line in input:
    v = line.split(' <-> ')
    node = int(v[0])
    graph[node] = list(map(int, v[1].split(', ')))
  return graph

def dfs(graph: Graph, node: Node, seen: set[Node]) -> None:
  if node in seen:
    return
  seen.add(node)

  for adj in graph[node]:
    dfs(graph, adj, seen)

def part1() -> None:
  graph = parseInput()
  print('nodes:', len(graph))

  seen: set[Node] = set()
  dfs(graph, 0, seen)
  print(len(seen))

def part2() -> None:
  graph = parseInput()
  print('nodes:', len(graph))

  remaining = set(graph.keys())
  c = 0
  while len(remaining) > 0:
    seen: set[Node] = set()
    # Choose an arbitrary element in the set and run a DFS from there.
    for n in remaining: break
    dfs(graph, n, seen)
    remaining.difference_update(seen)
    c += 1
  print(c)

part2()
