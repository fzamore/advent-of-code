from itertools import pairwise

data = open('day5.txt').read().splitlines()

def vowelCount(s: str) -> int:
  vowels = 'aeiou'
  return sum([s.count(v) for v in vowels])

def hasDoubleChar(s: str) -> bool:
  for ch1, ch2 in pairwise(s):
    if ch1 == ch2:
      return True
  return False

def isNice1(s: str) -> bool:
  if vowelCount(s) < 3:
    return False

  if not hasDoubleChar(s):
    return False

  bad = ['ab', 'cd', 'pq', 'xy']
  if any([b in s for b in bad]):
    return False

  return True

def hasMultiplePairs(s: str) -> bool:
  for i in range(len(s)):
    pair = s[i:i + 2]
    if pair in s[i + 2:]:
      return True
  return False

def hasSandwich(s: str) -> bool:
  for i in range(len(s) - 2):
    if s[i] == s[i + 2]:
      return True
  return False

def isNice2(s: str) -> bool:
  return hasMultiplePairs(s) and hasSandwich(s)

def part1() -> None:
  print(sum([isNice1(s) for s in data]))

def part2() -> None:
  print(sum([isNice2(s) for s in data]))

part2()
