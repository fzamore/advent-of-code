from collections import deque, namedtuple
from common.arraygrid import ArrayGrid
from common.shortestpath import dijkstra

input = open('day18.txt').read().splitlines()

Coords = tuple[int, int]

# Our state consists of a list of keys remaining (not picked up), and our
# current position (represented by string value - either "@" or a key).
State = namedtuple('State', ['keys', 'pos'])

# One position per robot and one set of keys for all robots in part 2.
MultiState = namedtuple('MultiState', ['positions', 'keys'])

def getAdjacentStates(
  adjacencies: dict[str, dict[str, tuple[int, list[str]]]],
  keys: tuple[str],
  currentKey: str,
) -> list[tuple[State, int]]:
  results = []
  keySet = set(keys)
  # Loop through all adjacencies from our current position.
  for key in adjacencies[currentKey]:
    dist, doorsInPath = adjacencies[currentKey][key]
    if key not in keySet:
      # We've already picked up this key. Skip it.
      continue

    if any([(door in keySet) for door in doorsInPath]):
      # If any of the doors in this path are still in our remaining keys
      # (i.e., we haven't yet picked up the key), we cannot move past this
      # door.
      continue

    # We've found a valid key to pick up. Remove it from our keys
    # remaining, and add the new state to our results list.
    nkeys = list(keys)
    nkeys.remove(key)
    results.append((State(tuple(nkeys), key), dist))

  return results

def explore(
  adjacencies: dict[str, dict[str, tuple[int, list[str]]]],
  start: str,
  keys: list[str],
) -> int:
  def getAdj(state: State) -> list[tuple[State, int]]:
    return getAdjacentStates(adjacencies, state.keys, state.pos)

  def isDone(state: State) -> bool:
    return len(state.keys) == 0

  _, steps = dijkstra(State(tuple(keys), start), getAdj, isDone)

  assert isinstance(steps, int) or steps.is_integer(), \
    'non-int returned from dijkstra: %s' % str(steps)
  return int(steps)

def explore2(
  adjacencies: dict[str, dict[str, tuple[int, list[str]]]],
  startPositions: list[str],
  keys: list[str],
) -> int:
  assert len(startPositions) == 4, 'wrong number of states'

  def getAdj(multiState: MultiState) -> list[tuple[MultiState, int]]:
    results = []
    for i, pos in enumerate(multiState.positions):
      for newState, steps in getAdjacentStates(adjacencies, multiState.keys, pos):
        # Move the robot to its new position.
        positions = list(multiState.positions)
        positions[i] = newState.pos

        # Collect the key.
        keys = list(multiState.keys)
        keys.remove(newState.pos)

        results.append((MultiState(tuple(positions), tuple(keys)), steps))
    return results

  def isDone(multiState: MultiState) -> bool:
    return len(multiState.keys) == 0

  _, steps = dijkstra(MultiState(tuple(startPositions), tuple(keys)), getAdj, isDone)

  assert isinstance(steps, int) or steps.is_integer(), \
    'non-int returned from dijkstra: %s' % str(steps)
  return int(steps)

# Generates a mapping of adjacencies for a given point (either a key or
# the origin). For each other key in the grid, the resulting dict contains
# an entry including thedistance from start to that key, and all doors
# along the path to that key.
def generateAdjacencies(grid: ArrayGrid, start: Coords) \
  -> dict[str, tuple[int, list[str]]]:
  results = {}
  seen = {start}
  q: deque[tuple[Coords, list[str], int]] = deque([(start, [], 0)])
  while len(q):
    (x, y), doors, depth = q.popleft()
    for nx, ny in grid.getAdjacentCoords(x, y, includeDiagonals=False):
      if (nx, ny) in seen:
        continue
      seen.add((nx, ny))
      v = grid.getValue(nx, ny)
      if v == '#':
        # We've hit a wall. Stop.
        continue

      # Make a copy of the doors list for this path.
      ndoors = doors.copy()
      if v.islower():
        # We encountered a key. Add the distance from the start to our
        # adjacencies list.
        results[v] = (depth + 1, doors)
      elif v.isupper():
        # We found a door. Add it to our list of doors for this path (and
        # make it lowercase to make checking easier in the future).
        ndoors.append(v.lower())

      # Keep moving through the grid.
      q.append(((nx, ny), ndoors, depth + 1))
  return results

def part1() -> None:
  grid = ArrayGrid.gridFromInput(input)
  w, h = grid.getWidth(), grid.getHeight()
  print('grid: %d x %d' % (w, h))
  grid.print2D()

  start = None
  keys: list[tuple[Coords, str]] = []
  for x in range(w):
    for y in range(h):
      v = str(grid.getValue(x, y))
      match v:
        case '@':
          start = (x, y), v
        case _ if v.islower():
          keys.append(((x, y), v))
        case _ if v.isupper(): pass
        case '.' | '#': pass
        case _: assert False, 'bad value in grid'

  assert start is not None, 'did not find start'
  assert len(keys) > 0, 'did not find keys'

  print('start:', start)
  print('keys:', len(keys), keys)
  print()

  toGenerate = [start] + keys
  print('generating adjacencies:', len(toGenerate))

  adjacencies = {}
  for pos, v in toGenerate:
    x, y = pos
    adj = generateAdjacencies(grid, pos)
    if v == '@':
      assert len(adj) == len(keys), 'not enough adjacencies generated'
    else:
      assert len(adj) == len(keys) - 1, 'not enough adjacencies generated'

    adjacencies[v] = adj

  print('exploring...')
  keyStrs = [k[1] for k in keys]
  print(explore(adjacencies, '@', keyStrs))

def part2() -> None:
  grid = ArrayGrid.gridFromInput(input)
  w, h = grid.getWidth(), grid.getHeight()
  print('grid: %d x %d' % (w, h))
  grid.print2D()

  starts = []
  keyLocations = {}
  for x in range(w):
    for y in range(h):
      v = grid.getValue(x, y)
      if v == '@':
        starts.append((x, y))
      elif v.islower():
        keyLocations[v] = x, y

  assert len(starts) in [1, 4], 'did not find correct number of starts'

  if len(starts) == 1:
    # Convert grid if necessary.
    print('fixing starts')
    start = starts[0]
    sx, sy = start
    for x, y in grid.getAdjacentCoords(sx, sy, includeDiagonals=True):
      assert grid.getValue(x, y) == '.', 'wrong grid pattern'
      if sx - x == 0 or sy - y == 0:
        grid.setValue(x, y, '#')
      else:
        grid.setValue(x, y, '@')
        starts.append((x, y))
    grid.setValue(sx, sy, '#')
    starts.pop(0)
    grid.print2D()

  print('starts:', starts)
  assert len(starts) == 4, 'bad number of starts'
  adjacencies = {}
  startPositions = []
  for i, start in enumerate(starts):
    adj = generateAdjacencies(grid, start)
    adjacencies[str(i)] = adj
    keys = []
    for key in adj:
      adjacencies[key] = generateAdjacencies(grid, keyLocations[key])
      keys.append(key)
    startPositions.append(str(i))

  print('adjacencies:',len(adjacencies))
  print('start positions:', startPositions)
  print()

  assert len(startPositions) == 4, 'bad number of states'
  print(explore2(adjacencies, startPositions, list(keyLocations.keys())))

part2()
