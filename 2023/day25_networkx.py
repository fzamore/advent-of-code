from itertools import combinations
import networkx as nx # type: ignore
import matplotlib.pyplot as plt

input = open('day25.txt').read().splitlines()

def part1() -> None:
  graph = nx.Graph()
  for line in input:
    parts = line.split(': ')
    s = parts[0]
    for n in parts[1].split():
      graph.add_edge(s, n, capacity=1.0, weight=1.0)

  print('vertices:', len(graph.nodes))
  print('edges:', len(graph.edges))
  print()

  # To print the graph, uncomment this.
  # nx.draw(graph)
  # plt.show()

  # Option 1: Use the Stoer-Wagner algorithm to find the minimum cut for
  # the entire graph.
  print('running stoer-wagner...')
  cut_value, (left, right) = nx.stoer_wagner(graph)
  assert cut_value == 3, 'cut_value is not 3: %d' % cut_value

  print('partition sizes:', len(left), len(right))
  print(len(left) * len(right))
  print()

  # Option 2: Try a minimum cut on all source-sink vertex combinations
  # until you find a cut_value of three edges.
  print('trying all source-sink combinations...')
  for v1, v2 in combinations(graph.nodes, 2):
    if v1 == v2:
      continue
    cut_value, (left, right) = nx.minimum_cut(graph, v1, v2)
    if cut_value == 3:
      print('found min cut:', len(left), len(right))
      print(len(left) * len(right))
      return
    else:
      print('  wrong min cut (%d edges). trying again...' % cut_value)

part1()
