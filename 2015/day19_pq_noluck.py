from heapq import heappop, heappush
from typing import Iterable

data = open('day19.txt').read().splitlines()

Replacements = list[tuple[str, str]]

def parse() -> tuple[Replacements, str]:
  start = None
  replacements = []
  for line in data:
    if line == '':
      continue

    if '=>' not in line:
      assert start is None, 'multiple starts'
      start = line
      continue

    # Al => ThRnFAr
    v = line.split(' => ')
    assert len(v) == 2, 'bad line'
    replacements.append((v[0], v[1]))

  assert start is not None, 'did not find start'
  return replacements, start

def getReplacementsFromRight(replacements: Replacements, start: str) -> Iterable[str]:
  for i in range(len(start), 0, -1):
    for src, dst in replacements:
      if start[i - len(src):i] == src:
        yield start[:i - len(src)] + dst + start[i:]

def part1() -> None:
  replacements, start = parse()
  print('start:', start)
  print(len(set(getReplacementsFromRight(replacements, start))))

def part2() -> None:
  replacements, target = parse()
  print('target:', len(target), target)

  reverseMap = [(y, x) for (x, y) in replacements]
  q: list[tuple[int, int, str]] = []
  heappush(q, (len(target), 0, target))
  while len(q) > 0:
    length, steps, node = heappop(q)
    assert length == len(node), 'bad queue management'

    if node == 'e':
      print('done.')
      print(steps)
      return

    # Stolen from Reddit. If you always choose the first replacement when
    # matching from the right, you'll never back yourself into a corner
    # and will always be able to continue.
    for rep in getReplacementsFromRight(reverseMap, node):
      heappush(q, (len(rep), steps + 1, rep))
      break

  assert False, 'did not find answer'

part2()
