from collections import defaultdict
from typing import Iterable, Optional

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

def solveViaDfs(reverseMap: dict[str, str], molecule: str, count: int = 0) -> Optional[int]:
  if len(molecule) == 2:
    # Base case. We will never get to 1, because we removed the 'e' rule from the map.
    print('done:', count + 1)
    # Add 1 to count because we need to do one more translation at the end to get to 'e'.
    return count + 1

  # If we find any translations that apply to this string, recur on them.
  for key in reverseMap:
    i = molecule.find(key)
    if i == -1:
      continue
    n = molecule[:i] + reverseMap[key] + molecule[(i + len(key)):]
    if (result := solveViaDfs(reverseMap, n, count + 1)):
      return result

  return None

def part1() -> None:
  replacements, start = parse()
  print('start:', start)
  print(len(set(getReplacements(replacements, start))))

def part2() -> None:
  target = data[-1]
  print('target:', target, len(target))

  # I copied this approach from Reddit.

  # Rn, Y, and Ar are special, because they don't appear on the left side
  # of any translation. Replace them with special characters in the
  # string, and replace every other token with the same character. The
  # special characters cannot appear anywhere else in the string before
  # translation.
  Rn, Y, Ar, X = '(', ',', ')', 'X'
  replacements = {
    'Rn': Rn,
    'Y': Y,
    'Ar': Ar,
  }
  for k in replacements:
    target = target.replace(k, replacements[k])
  chars = []
  for ch in target:
    if ch in replacements.values():
      chars.append(ch)
    elif ch.isupper():
      chars.append(X)
  target = ''.join(chars)
  print('target after translation:', target)

  # This formula was copied from Reddit.
  print('formula:', len(target) - target.count(Ar) - target.count(Rn) - 2 * target.count(Y) - 1)

  # This is a simplified version of the input translations, but they have
  # been reversed (so we are going from bigger to smaller). This was
  # copied from Reddit. In this approach we completely ignore the
  # translation from the input.
  # X => XX | X(X) | X(X,X) | X(X,X,X)
  reverseKeys = [
    (X, X), # XX
    (X, Rn, X, Ar), # X(X)
    (X, Rn, X, Y, X, Ar), # X(X,X)
    (X, Rn, X, Y, X, Y, X, Ar), # X(X,X,X)
  ]
  reverseMap = {}
  for key in reverseKeys:
    reverseMap[''.join(key)] = X

  # There is only one route from start to finish, so we don't need to
  # worry about minimizing anything.
  print(solveViaDfs(reverseMap, target))

part2()
