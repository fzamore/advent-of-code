from collections import deque, namedtuple
from common.arraygrid import ArrayGrid
from common.shortestpath import dijkstra

input = open('day18.txt').read().splitlines()

Coords = tuple[int, int]

# Our state consists of a list of keys remaining (not picked up), and our
# current position.
State = namedtuple('State', ['keys', 'pos'])

def getAdjacentStates(
  adjacencies: dict[Coords, dict[Coords, tuple[int, list[Coords]]]],
  state: State,
  keys: dict[Coords, str],
  doors: dict[Coords, str],
):
  results = []
  for keypos in adjacencies[state.pos]:
    dist, doorsInPath = adjacencies[state.pos][keypos]
    if keypos not in state.keys:
      # We've already picked up this key. Skip it.
      continue

    remainingKeyvals = set(
      [keys[k] for k in state.keys]
    )
    lockedDoor = False
    for doorpos in doorsInPath:
      doorval = doors[doorpos]
      if doorval in remainingKeyvals:
        lockedDoor = True
        break
    if lockedDoor:
      # We've encountered a locked door.
      continue

    # We've found a valid key to pick up. Remove it from our keys
    # remaining, and add the new state to our results list.
    nkeys = list(state.keys)
    nkeys.remove(keypos)
    results.append((State(tuple(nkeys), keypos), dist))

  return results

def explore(
  adjacencies: dict[Coords, dict[Coords, tuple[int, list[Coords]]]],
  start: Coords,
  keys: dict[Coords, str],
  doors: dict[Coords, str],
) -> int:
  def getAdj(state: State) -> list[tuple[State, int]]:
    return getAdjacentStates(adjacencies, state, keys, doors)

  def isDone(state: State) -> bool:
    return len(state.keys) == 0

  _, steps = dijkstra(State(tuple(keys.keys()), start), getAdj, isDone)

  assert isinstance(steps, int) or steps.is_integer(), \
    'non-int returned from dijkstra: %s' % str(steps)
  return int(steps)

# Generates a mapping of adjacencies for a given point (either a key or
# the origin). For each other key in the grid, the resulting dict contains
# an entry including thedistance from start to that key, and all doors
# along the path to that key.
def generateAdjacencies(grid: ArrayGrid, start: Coords) \
  -> dict[Coords, tuple[int, list[Coords]]]:
  results = {}
  seen = {start}
  q: deque[tuple[Coords, list[Coords], int]] = deque([(start, [], 0)])
  while len(q):
    (x, y), doors, depth = q.popleft()
    for nx, ny in grid.getAdjacentCoords(x, y, includeDiagonals=False):
      if (nx, ny) in seen:
        continue
      seen.add((nx, ny))
      v = grid.getValue(nx, ny)
      if v == '#':
        continue
      # Make a copy of the doors list for this path.
      ndoors = doors.copy()
      if v.islower():
        # We encountered a key. Add the distance from the start to our
        # adjacencies list.
        results[(nx, ny)] = (depth + 1, doors)
      elif v.isupper():
        # We found a door. Add it to our list of doors for this path.
        ndoors.append((nx, ny))
      # Keep moving through the grid.
      q.append(((nx, ny), ndoors, depth + 1))
  return results

def part1() -> None:
  grid = ArrayGrid.gridFromInput(input)
  w, h = grid.getWidth(), grid.getHeight()
  print('grid: %d x %d' % (w, h))
  grid.print2D()

  start = None
  keys: dict[Coords, str] = {}
  doors: dict[Coords, str] = {}
  for x in range(w):
    for y in range(h):
      v = str(grid.getValue(x, y))
      match v:
        case '@':
          start = x, y
        case _ if v.islower():
          keys[(x,y)] = v
        case _ if v.isupper():
          # Make the doors lowercase to make checking easier in the future.
          doors[(x,y)] = v.lower()
        case '.' | '#': pass
        case _: assert False, 'bad value in grid'

  assert start is not None, 'did not find start'
  assert len(keys) > 0, 'did not find keys'
  assert len(doors) > 0, 'did not find doors'

  print('start:', start)
  print('keys:', len(keys), keys)
  print('doors:', len(doors), doors)
  print()

  toGenerate = [start] + list(keys.keys())
  print('generating adjacencies:', len(toGenerate))

  adjacencies = {}
  for pos in toGenerate:
    x, y = pos
    adj = generateAdjacencies(grid, pos)
    adjacencies[pos] = adj
    if pos == start:
      assert len(adj) == len(keys), 'not enough adjacencies generated'
    else:
      assert len(adj) == len(keys) - 1, 'not enough adjacencies generated'

  print('exploring...')
  print(explore(adjacencies, start, keys, doors))

part1()
