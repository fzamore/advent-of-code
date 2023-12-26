from collections import defaultdict

input = open('day25.txt').read().splitlines()

def part1() -> None:
  vertices = set()
  adjacentVertices = defaultdict(list)
  for line in input:
    parts = line.split(': ')
    s = parts[0]
    vertices.add(s)
    for n in parts[1].split():
      vertices.add(n)
      adjacentVertices[s].append(n)
      adjacentVertices[n].append(s)

  print('vertex count:', len(vertices))
  print('edge count:', sum([len(adjacentVertices[v]) for v in vertices]) // 2)

  # I stole this algorithm from Reddit.
  #
  # Maintain a set of vertices not connected to the rest of the graph. For
  # each such vertex, keep track of how many adjacent edges it has to the
  # rest of the graph (i.e., to vertices not in this set). Thus, the sum
  # of all of these values is the number of edges between the set and the
  # rest of the graph. We start wtih all vertices in the set (each with
  # value 0), and we remove them from the set until there are three edges
  # from the set to the rest of the set.
  unconnectedSet = dict([(v, 0) for v in vertices])

  while sum(unconnectedSet.values()) != 3:
    if len(unconnectedSet) == 0:
      # It is possible that the algorithm will fail (e.g., if the first
      # node chosen is one of the connection point between the two
      # disconnected sets). This seems to be much less likely in the real
      # input. If this happens, run the algorithm again.
      print()
      print('*** Unlucky. The algorithm failed. Please run it again. ***')
      print()
      return

    # Choose the "most connected" node of the unconnected set, i.e., the
    # node with the most number of edges to vertices outside the set. It
    # makes sense that the most connected node would be the least likely
    # to be part of the "connected" set, but I don't understand why it's
    # necessary to choose the max-value node (and why a random node won't
    # work).
    v = max(unconnectedSet, key=unconnectedSet.__getitem__)

    # Remove the node from the unconnected set and increase the value of
    # all adjacent nodes still in the unconnected set.
    del unconnectedSet[v]
    for adjNode in adjacentVertices[v]:
      if adjNode in unconnectedSet:
        unconnectedSet[adjNode] += 1

  s1 = len(unconnectedSet)
  s2 = len(vertices) - s1
  print(s1, s2)
  print(s1 * s2)

part1()
