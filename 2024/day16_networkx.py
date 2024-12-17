from common.arraygrid import ArrayGrid
import networkx as nx # type: ignore

input = open('day16.txt').read().splitlines()

Coords = tuple[int, int]

def parseInput() -> tuple[ArrayGrid, Coords, Coords]:
  start, end = None, None
  grid = ArrayGrid.gridFromInput(input)
  for x, y, v in grid.getItems():
    if v == 'S':
      start = x, y
    if v == 'E':
      end = x, y
  assert (start is not None) and (end is not None), 'did not find start and end'
  return grid, start, end

def buildGraph(grid: ArrayGrid, start: Coords, end: Coords) -> nx.Graph:
  graph = nx.Graph()
  for x, y, v in grid.getItems():
    if v == '#':
      continue

    for ax, ay in grid.getAdjacentCoords(x, y):
      av = grid.getValue(ax, ay)
      if av == '#':
        continue

      adx, ady = ax - x, ay - y
      # For each node, attempt to add an edge for edge incoming direction.
      for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        prevx, prevy = x - dx, y - dy
        if (prevx, prevy) == (ax, ay):
          # No u-turns.
          continue

        if (x, y) != start and grid.getValue(prevx, prevy) == '#':
          # Don't allow traversing from an incoming wall (unless it's the start).
          continue

        weight = 1
        if (dx, dy) != (adx, ady):
          # A turn.
          weight += 1000

        graph.add_edge(((x, y), (dx, dy)), ((ax, ay), (adx, ady)), weight=weight)

  # Assume that the target is only accessible via the left and below. Add
  # a special edge of weight zero for both incoming states so we have a
  # single end node.
  graph.add_edge((end, (1, 0)), (end, (0, 0)), weight=0)
  graph.add_edge((end, (0, -1)), (end, (0, 0)), weight=0)

  print('verticies:', len(graph.nodes))
  print('edges:', len(graph.edges))

  return graph

def part1() -> None:
  grid, start, end = parseInput()
  print('start/end:', start, end)

  graph = buildGraph(grid, start, end)
  print(nx.shortest_path_length(graph, (start, (1, 0)), (end, (0, 0)), weight='weight'))

def part2() -> None:
  grid, start, end = parseInput()
  print('start/end:', start, end)

  graph = buildGraph(grid, start, end)

  shortestPaths = list(nx.all_shortest_paths(graph, (start, (1, 0)), (end, (0, 0)), weight='weight'))
  print('shortestPaths:', len(shortestPaths))
  allNodes = set()
  for path in shortestPaths:
    allNodes.update([n[0] for n in path])
  print(len(allNodes))

part2()
