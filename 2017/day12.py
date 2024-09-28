from common.graphtraversal import dfs, getConnectedComponents

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

def part1() -> None:
  graph = parseInput()
  print('nodes:', len(graph))

  count = 0
  def visit(node: Node) -> None:
    nonlocal count
    count += 1

  dfs(0, lambda node: graph[node], visitNode = visit)
  print(count)

def part2() -> None:
  graph = parseInput()
  print('nodes:', len(graph))

  print(len(getConnectedComponents(graph.keys(), lambda node: graph[node])))

part2()
