from collections import defaultdict, namedtuple
from typing import Iterable
from common.graphtraversal import bfs
from itertools import combinations

input = open('day11.txt').read().splitlines()

# The state is a tuple containing the floor the elevator is on, as well as
# a list (technically a tuple) of pairs representing the floors that a
# given generator/microchip are on. The name of the generator/microchip pair
# is intentionally omitted from the state, as all names are treated the
# same. We sort the list of pairs so that equivalent states are treated
# the same.
State = namedtuple('State', ['elevator', 'pairs'])
Pair = tuple[int, int]

# A set of items on each floor (floors are zero-indexed).
Floors = list[set[str]]

def parseFloor(line: str) -> int:
  # Floors are zero-indexed.
  d = {
    'first': 0,
    'second': 1,
    'third': 2,
    'fourth': 3,
  }
  for k in d:
    if k in line:
      return d[k]
  assert False, 'bad floor'

def parseInput() -> State:
  pairsByName: dict[str, Pair] = defaultdict(lambda: (-1, -1))
  for line in input:
    floor = parseFloor(line)
    if 'nothing relevant' in line:
      continue

    v = line.split()
    for i, w in enumerate(v):
      isChip = 'compatible' in w
      if isChip:
        name = w.split('-')[0]
      elif 'generator' in w:
        name = v[i - 1]
      else:
        continue

      assert name is not None, 'no name in input line'
      if isChip:
        pairsByName[name] = pairsByName[name][0], floor
      else:
        pairsByName[name] = floor, pairsByName[name][1]

  return State(0, tuple(sorted(pairsByName.values())))

def getPossibleDstFloors(floor: int) -> list[int]:
  match floor:
    case 0: return [1]
    case 1: return [0, 2]
    case 2: return [1, 3]
    case 3: return [2]
    case _: assert False, 'bad floor'

def canChipExistOnFloor(items: Iterable[str], item: str) -> bool:
  assert item[-1] == 'm', 'item must be chip'

  hasOtherGen = False
  hasSameGen = False
  for i in items:
    if i[-1] != 'g':
      continue

    if i[:-2] != item[:-2]:
      hasOtherGen = True
    else:
      hasSameGen = True

  if not hasOtherGen:
    # No other generators. Everything fine
    return True

  # Need a same generator to protect against the other generator.
  return hasSameGen

def isValidFloors(floors: Floors) -> bool:
  for items in floors:
    for item in items:
      if item[-1] == 'm' and not canChipExistOnFloor(items, item):
        return False
  return True

def moveItemsToFloorIfPossible(floors: Floors, elevator: int, floor: int, items: list[str]):
  nfloors = [set(x) for x in floors]
  for x in ['e'] + items:
    nfloors[elevator].remove(x)
    nfloors[floor].add(x)

  if not isValidFloors(nfloors):
    return None

  return nfloors

def getPossibleItemsToMove(itemsOnElevatorFloor: Iterable[str]) -> Iterable[list[str]]:
  # Try to move a single item in the elevator.
  for item in itemsOnElevatorFloor:
    yield [item]

  # Try to move two items in the elevator.
  for item1, item2 in combinations(itemsOnElevatorFloor, 2):
    yield [item1, item2]

def getAdjacentFloors(floors: Floors, elevator: int) -> Iterable[Floors]:
  assert len(floors[elevator]) > 1, 'elevator stuck'

  itemsOnElevatorFloor = [x for x in floors[elevator] if x != 'e']
  for floor in getPossibleDstFloors(elevator):
    for itemsToMove in getPossibleItemsToMove(itemsOnElevatorFloor):
      if (nfloors := moveItemsToFloorIfPossible(floors, elevator, floor, itemsToMove)) is not None:
        yield nfloors

def stateToFloors(state: State) -> Floors:
  floors: Floors = [set(), set(), set(), set()]
  for i, (g, c) in enumerate(state.pairs):
    floors[g].add('%d-g' % i)
    floors[c].add('%d-m' % i)
  floors[state.elevator].add('e')
  return floors

def floorsToState(floors: Floors) -> State:
  tempstate: dict[str, Pair] = defaultdict(lambda: (-1, -1))
  elevator = None
  for floor, floorItems in enumerate(floors):
    for item in floorItems:
      if item == 'e':
        elevator = floor
        continue

      name = item[0]
      match item[2]:
        case 'g':
          tempstate[name] = floor, tempstate[name][1]
        case 'm':
          tempstate[name] = tempstate[name][0], floor
        case _:
          assert False, 'bad type'

  assert elevator is not None, 'did not find new elevator floor'
  return State(elevator, tuple(sorted(tempstate.values())))

def getAdjacentState(state: State) -> Iterable[State]:
  # Convert State to Floors, which is easier to work with.
  adjFloors = getAdjacentFloors(stateToFloors(state), state.elevator)
  for floors in adjFloors:
    yield floorsToState(floors)

def isDone(state: State) -> bool:
  for (genFloor, chipFloor) in state.pairs:
    if genFloor != 3 or chipFloor != 3:
      return False
  return True

def part1() -> None:
  state = parseInput()
  print('initial state:', state)

  result = bfs(state, getAdjacentState, isEndNode=isDone)
  print(max(result.values()))

def part2() -> None:
  state = parseInput()

  # Add two more pairs on the bottom floor.
  pairs = list(state.pairs)
  pairs.append((0, 0))
  pairs.append((0, 0))
  state = State(state.elevator, tuple(sorted(pairs)))

  print('initial state:', state)

  result = bfs(state, getAdjacentState, isEndNode=isDone)
  print(max(result.values()))

part2()
