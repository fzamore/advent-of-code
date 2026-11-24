from collections import Counter
from itertools import chain

Pair = tuple[int, int]

def parseLine(line: str) -> list[Pair]:
  pairs = []
  for item in line.split():
    a = int(item[0])
    b = int(item[2])
    pairs.append((a, b) if item[1] == '>' else (b, a))
  return pairs

def parse(filename: str) -> list[list[Pair]]:
  lines = open(filename).read().splitlines()
  return list(map(parseLine, lines))

# Finds the hardest element by searching for an element that never appears softer than any other element.
def findHardest(pairs: list[Pair]) -> int:
  # This counter counts the number of times an element is softer than another one.
  c = Counter(b for (a, b) in pairs)
  for a, _ in pairs:
    if a not in c:
      return a

  assert False, 'did not find hardest'

def solveGroup(pairs: list[Pair]) -> int:
  all = set(chain.from_iterable(pairs))
  working = pairs.copy()

  r = []
  while len(all) > 1:
    hardest = findHardest(working)
    all.remove(hardest)
    r.append(str(hardest))
    # Remove all pairs containing the hardest element from our working set.
    working = [(a, b) for (a, b) in working if a != hardest]

  # We only have one element left.
  r.append(str(all.pop()))
  return int(''.join(r))

def solve(filename: str) -> int:
  groups = parse(filename)
  print('groups:', len(groups))

  s = 0
  for group in groups:
    ans = solveGroup(group)
    print('group:', ans)
    s += ans
  return s

def part1() -> None:
  print(solve('quest2.1.txt'))

def part2() -> None:
  print(solve('quest2.2.txt'))

def part3() -> None:
  print(solve('quest2.3.txt'))

part3()
