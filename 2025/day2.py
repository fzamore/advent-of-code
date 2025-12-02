from functools import cache
from itertools import batched
from math import sqrt
from typing import Collection, Iterable

data = open('day2.txt').read()

def parse() -> Iterable[tuple[int, int]]:
  ranges = data.split(',')
  for rng in ranges:
    start, end = map(int, rng.split('-'))
    yield start, end

def isInvalid(v: int, d: int = 2) -> bool:
  s = str(v)
  n = len(s)
  if n % d != 0:
    return False

  # Split up into equally-sized chunks, and return whether all chunks are equal.
  parts = batched(s, n // d)
  first = next(parts)
  for part in parts:
    if first != part:
      return False
  return True

def isInvalidAny(v: int) -> bool:
  return any(isInvalid(v, f) for f in factors(len(str(v))))

@cache
def factors(n: int) -> Collection[int]:
  result = set()
  for i in range(1, int(sqrt(n)) + 1):
    if n % i == 0:
      result.add(i)
      result.add(n // i)
  # Don't include 1 in the result, as that would include every value.
  result.remove(1)
  return result

def part1() -> None:
  ranges = list(parse())
  print('ranges:', len(ranges))
  ans = 0
  for start, end in ranges:
    ans += sum(i if isInvalid(i) else 0 for i in range(start, end + 1))
  print(ans)

def part2() -> None:
  ranges = list(parse())
  print('ranges:', len(ranges))
  ans = 0
  for start, end in ranges:
    ans += sum(i if isInvalidAny(i) else 0 for i in range(start, end + 1))
  print(ans)

part2()
