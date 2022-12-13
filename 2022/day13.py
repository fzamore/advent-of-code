from enum import Enum
import json

input = open('day13.txt').read().split("\n\n")

class Cmp(Enum):
  CORRECT = -1
  UNKNOWN = 0
  INCORRECT = 1

def compareInts(v1: int, v2: int) -> Cmp:
  if v1 < v2: return Cmp.CORRECT
  elif v1 > v2: return Cmp.INCORRECT
  else: return Cmp.UNKNOWN

def compareValues(v1: int | list, v2: int | list) -> Cmp:
  if isinstance(v1, int) and isinstance(v2, int):
    return compareInts(v1, v2)

  list1 = [v1] if isinstance(v1, int) else v1
  list2 = [v2] if isinstance(v2, int) else v2
  return compareLists(list1, list2)

def compareLists(
  list1: list[int | list],
  list2: list[int | list],
) -> Cmp:
  i = 0
  while i < len(list1) or i < len(list2):
    if i >= len(list1):
      # left side ran out of items first
      return Cmp.CORRECT

    if i >= len(list2):
      # right side ran out of items first
      return Cmp.INCORRECT

    result = compareValues(list1[i], list2[i])
    if result != Cmp.UNKNOWN:
      return result
    i += 1

  return Cmp.UNKNOWN

def part1():
  pairs = []
  for chunk in input:
    lines = chunk.splitlines()
    assert len(lines) == 2, 'invalid chunk: %s' % chunk
    pairs.append((
      json.loads(lines[0]),
      json.loads(lines[1]),
    ))

  print('number of pairs:', len(pairs))

  sum = 0
  i = 1
  for list1, list2 in pairs:
    result = compareLists(list1, list2)
    assert result != Cmp.UNKNOWN, 'bad result: %s, %s' %(list1, list2)
    print(i, result)
    if result == Cmp.CORRECT:
      sum += i
    i += 1
  print(sum)

part1()
