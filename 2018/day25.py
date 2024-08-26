from itertools import combinations
from collections import defaultdict

input = open('day25.txt').read().splitlines()

Point = tuple[int, int, int, int] # 4D point.
Edges = dict[Point, list[Point]]

def manH(p1: Point, p2: Point) -> int:
  w1, x1, y1, z1 = p1
  w2, x2, y2, z2 = p2
  return abs(w2 - w1) + abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1)

# Builds a graph of points such that there is an edge between two points
# if their Manhattan distance is three or less. Returns a dict where the
# key is the point and the value is a list of points for which there is an
# edge.
def buildGraph(points: list[Point]) -> Edges:
  edges = defaultdict(list)
  for p1, p2 in combinations(points, 2):
    if manH(p1, p2) <= 3:
      edges[p1].append(p2)
      edges[p2].append(p1)
  return edges

# Runs a DFS over the given graph of edges starting at the given point.
def dfs(p: Point, edges: Edges, seen: set[Point]) -> None:
  seen.add(p)
  for adj in edges[p]:
    if adj not in seen:
      dfs(adj, edges, seen)

def part1() -> None:
  points = []
  for line in input:
    w, x, y, z = map(int, line.split(','))
    points.append((w, x, y, z))
  print('points:', len(points))

  edges = buildGraph(points)

  # We need to find the number of connected components in the graph. To do
  # so, we run a DFS on each point in the graph, but we skip points that
  # have already been seen by a previous DFS. Each time we encounter a new
  # point, we have a new satellite (connected component).
  satellites = 0
  seen: set[Point] = set()
  for point in points:
    if point in seen:
      continue
    dfs(point, edges, seen)
    print('points seen:', len(seen))
    satellites += 1

  print(satellites)

part1()
