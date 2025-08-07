from collections import defaultdict
from typing import Iterable

data = open('day19.txt').read().splitlines()

Replacements = dict[str, set[str]]

def parse() -> tuple[Replacements, str]:
  start = None
  replacements = defaultdict(set)
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
    replacements[v[0]].add(v[1])

  assert start is not None, 'did not find start'
  return replacements, start

def getReplacements(replacements: Replacements, start: str) -> Iterable[str]:
  for i in range(len(start)):
    endi = None
    if start[i] in replacements:
      # Single-char sequence.
      endi = i + 1
    elif i < len(start) - 1 and start[i:i + 2] in replacements:
      # Two-char sequence.
      endi = i + 2

    if endi is None:
      continue

    src = start[i:endi]
    for dst in replacements[src]:
      yield start[:i] + dst + start[endi:]

def part1() -> None:
  replacements, start = parse()
  print('start:', start)
  print(len(set(getReplacements(replacements, start))))

part1()
