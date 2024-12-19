import re
from typing import Optional

input = open('day19.txt').read().splitlines()

def parseInput() -> tuple[list[str], list[str]]:
  towels = None
  patterns: list[str] = []
  for line in input:
    if line == '':
      continue
    if towels is None:
      towels = line.split(', ')
    else:
      patterns.append(line)

  assert towels is not None, 'did not find towels'
  return towels, patterns

def findIsolatedU(s: str, start: int = 0) -> Optional[int]:
  n = len(s)
  for i in range(start, min(start + n, n)):
    if s[i] != 'u':
      continue
    if i > 0 and s[i - 1] == 'u':
      continue
    if i < n - 1 and s[i + 1] == 'u':
      continue
    return i
  return None

def hasIsolatedU(s: str) -> bool:
  return findIsolatedU(s) is not None

def part1() -> None:
  towels, patterns = parseInput()
  print('data:', len(towels), len(patterns))

  for p in patterns:
    assert 'u' in p, 'no u in pattern'
    if not hasIsolatedU(p):
      print('bad pattern:', p)

  # Our list of towels contains r, g, b, w, uu, and uuu, which are very useful,
  # so we can filter out all other towels that don't have an isolated u.
  specialTowels = ['r', 'g', 'b', 'w', 'uu', 'uuu']
  for st in specialTowels:
    assert st in towels, 'special towel not found in towels'

  towels = [t for t in towels if hasIsolatedU(t)]
  towels.extend(specialTowels)
  print('filtered towels:', len(towels))
  print(towels)

  mx = max([len(t) for t in towels])
  print('max towel length:', mx)

  # This regex-based approach takes ~13 seconds with pypy.
  repattern = '^(%s)+$' % '|'.join(['%s' % t for t in towels])
  print('repattern:', repattern)

  ans = 0
  for i, p in enumerate(patterns):
    print('checking:', i, p)
    if re.match(repattern, p) is not None:
      ans += 1
  print(ans)

part1()
