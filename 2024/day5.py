from common.ints import ints
from collections import defaultdict
from functools import cmp_to_key

input = open('day5.txt').read().splitlines()

Graph = dict[int, list[int]]
Update = list[int]

# I didn't like this problem because there are cycles in the page ordering
# rules; i.e., there is no total ordering of pages. Reddit claims that
# within each update, any applicable rules don't create a cycle (without
# which I don't think there would be a solution). But still, it seems lame
# that the input is not a DAG.

def parseInput() -> tuple[Graph, list[Update]]:
  graph = defaultdict(list)
  updates = []

  for line in input:
    if '|' in line:
      v1, v2 = ints(line)
      graph[v1].append(v2)
    elif line != '':
      updates.append(ints(line))

  print('nodes:', len(graph))
  print('updates:', len(updates))
  return graph, updates

def isReachable(graph: Graph, v1: int, v2: int) -> bool:
  return v2 in graph[v1]

def isValidUpdate(graph: Graph, update: Update) -> bool:
  assert len(update) % 2 == 1, 'update length should be odd'

  # This only considers adjacent nodes in the update, which is sufficient,
  # assuming there are no cycles in any rules that apply to this update.
  for i in range(len(update) - 1):
    v1 = update[i]
    v2 = update[i + 1]
    if v2 not in graph[v1]:
      # Lame that we don't need to consider transitivity here.
      assert v1 in graph[v2], 'for every two pages, there must be a rule between them'
      return False
  return True

def part1() -> None:
  graph, updates = parseInput()
  ans = sum([u[len(u) // 2] for u in updates if isValidUpdate(graph, u)])
  print(ans)

def part2() -> None:
  graph, updates = parseInput()

  invalidUpdates = [u for u in updates if not isValidUpdate(graph, u)]

  # Comparator function.
  def c(v1: int, v2: int) -> int:
    if v2 in graph[v1]:
      return -1
    elif v1 in graph[v2]:
      return 1
    else:
      assert False, 'rule must exist between each pair of values'

  ans = 0
  for update in invalidUpdates:
    validUpdate = sorted(update, key=cmp_to_key(c))
    ans += validUpdate[len(validUpdate) // 2]
  print(ans)

part2()
