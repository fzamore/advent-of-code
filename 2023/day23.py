from typing import Optional
from common.arraygrid import ArrayGrid

input = open('day23.txt').read().splitlines()

Coords = tuple[int, int]

def canMove(cur: Coords, next: Coords, nextValue: str) -> bool:
  if nextValue == '.':
    return True
  elif nextValue == '#':
    return False

  allowed = {
    '<': (-1, 0),
    '>': (1, 0),
    'v': (0, 1),
    '^': (0, -1),
  }
  x, y = cur
  nx, ny = next
  dx, dy = nx - x, ny - y
  return (dx, dy) == allowed[nextValue]

def getAdjacentCoords(
  grid: ArrayGrid,
  cur: Coords,
  prev: Optional[Coords],
  visited: set[Coords],
) -> list[Coords]:
  results = []
  x, y = cur
  for next in grid.getAdjacentCoords(x, y):
    if next == prev or next in visited:
      continue
    nx, ny = next
    if canMove(cur, next, grid.getValue(nx, ny)):
      results.append(next)
  return results

# Skips ahead until there is a choice to make.
def skipAheadToChoice(
  grid: ArrayGrid,
  cur: Coords,
  prev: Optional[Coords],
  path: list[Coords],
  visited: set[Coords],
) -> tuple[Coords, list[Coords]]:
  adj = getAdjacentCoords(grid, cur, prev, visited)
  while len(adj) == 1:
    prev = cur
    cur = adj[0]
    path.append(cur)
    visited.add(cur)
    adj = getAdjacentCoords(grid, cur, prev, visited)
  return cur, adj

def findLongestPath(
  grid: ArrayGrid,
  cur: Coords,
  prev: Optional[Coords],
  end: Coords,
  visited: set[Coords] = set(),
) -> Optional[list[Coords]]:
  assert cur not in visited, 'already visited node: %s' % str(cur)
  visited.add(cur)
  path = [cur]

  # As long as there is exactly one way to go, keep moving that way
  # without recurring (to not increase the recursion stack depth).
  cur, adj = skipAheadToChoice(grid, cur, prev, path, visited)
  if cur == end:
    return path

  longestLen = -1
  longestPath = None
  for next in adj:
    npath = findLongestPath(grid, next, cur, end, visited.copy())
    if npath is None:
      continue
    if len(npath) > longestLen:
      longestLen = len(npath)
      longestPath = npath.copy()

  if longestPath is None:
    return None

  path.extend(longestPath)
  return path

def getSkipAheadNodes(
  grid: ArrayGrid,
  cur: Coords,
) -> list[tuple[Coords, int]]:
  x, y = cur
  assert grid.getValue(x, y) != '#', 'non-empty cell'

  result = []
  adj = [c for c in grid.getAdjacentCoords(x, y) \
         if grid.getValue(c[0], c[1]) == '.']
  for ax, ay in adj:
    if len(adj) == 2:
      # We have no choice. Do not add this node to the graph.
      continue
    path: list[Coords] = [(ax, ay)]
    next, _ = skipAheadToChoice(grid, (ax, ay), (x, y), path, set())
    result.append((next, len(path)))
  return result

def countLongestPathGraph(
  graph: dict[Coords, list[tuple[Coords, int]]],
  cur: Coords,
  prev: Optional[Coords],
  end: Coords,
  pathLen: int,
  visited: set[Coords] = set(),
) -> int:
  assert cur not in visited, 'already visited node: %s' % str(cur)
  visited.add(cur)
  if cur == end:
    return pathLen

  longestLen = -1
  for next, nextLen in graph[cur]:
    if next == prev or next in visited:
      continue
    longestLen = max(
      longestLen,
      countLongestPathGraph(
        graph,
        next,
        cur,
        end,
        pathLen + nextLen,
        visited.copy(),
      ),
    )
  return longestLen

def part1() -> None:
  grid = ArrayGrid.gridFromInput(input)
  w, h, = grid.getWidth(), grid.getHeight()
  print('grid: (%d x %d)' % (w, h))
  grid.print2D()

  start = (1, 0)
  end = (w - 2, h - 1)
  print('start:', start)
  print('end:', end)

  path = findLongestPath(grid, start, None, end)
  if path is not None:
    for x, y in path:
      v = 'S' if (x, y) == start else 'O'
      grid.setValue(x, y, v)
    grid.print2D()
    print(len(path) - 1)

def part2() -> None:
  grid = ArrayGrid.gridFromInput(input)
  w, h, = grid.getWidth(), grid.getHeight()
  print('grid: (%d x %d)' % (w, h))

  # Get rid of all slopes, so they will be ignored.
  for y in range(h):
    for x in range(w):
      if grid.getValue(x, y) in ['<', '>', '^', 'v']:
        grid.setValue(x, y, '.')

  start = (1, 0)
  end = (w - 2, h - 1)
  print('start:', start)
  print('end:', end)

  grid.print2D()

  # Preprocess the grid by reducing it to only nodes where there is a
  # choice involved. For each such "choice" node in the graph, we store
  # its adjacent "choice" nodes as (coords, pathLength) tuples (where
  # pathLength is the length of the path between the two nodes in the
  # original grid).
  graph = {}
  for y in range(h):
    for x in range(w):
      if grid.getValue(x, y) == '#':
        continue
      nodes = getSkipAheadNodes(grid, (x, y))
      if len(nodes) > 0:
        graph[(x, y)] = nodes
  print('graph nodes:', len(graph))

  print(countLongestPathGraph(graph, start, None, end, 0))

part2()
