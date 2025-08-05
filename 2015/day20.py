from math import floor, sqrt
from typing import Iterable, Optional

data = open('day20.txt').read()

def getFactors(n: int, limit: Optional[int] = None) -> Iterable[int]:
  for i in range(1, floor(sqrt(n)) + 1):
    if n % i == 0:
      if limit is None or limit * i >= n:
        yield i
      if limit is None or limit * (n // i) >= n:
        yield n // i

def compute(n: int, k: int = 10, limit: Optional[int] = None) -> int:
  return k * sum(getFactors(n, limit))

def part1() -> None:
  target = int(data)
  print('target:', target)

  # Stupidly slow.
  i = 1
  while (s := compute(i)) < target:
    i += 1
  print('done:', i, s)
  print(i)

def part2() -> None:
  target = int(data)
  print('target:', target)

  # Stupidly slow.
  n = 50
  k = 11
  i = 1
  while (s := compute(i, k, n)) < target:
    i += 1
  print('done:', i, s)
  print(i)

part2()
