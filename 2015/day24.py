from itertools import combinations
from math import prod
from typing import Optional

data = open('day24.txt').read().splitlines()

# Solves the puzzle with a fairly simple algorithm. We only care about the
# first group and do not care at all about the remaining groups. We
# iterate over increasing group sizes (starting at 1) until we find one
# that matches. Of all the groups that match at that size, we pick the one
# with lowest QE.
def solve(packages: list[int], numgroups: int) -> int:
  total = sum(packages)
  assert total % numgroups == 0, 'groups do not divide evenly'
  expectedSum = total // numgroups

  for n in range(1, len(packages)):
    print('trying:', n)
    ans: Optional[int] = None
    for g1 in combinations(packages, n):
      if sum(g1) != expectedSum:
        continue

      p = prod(g1)
      ans = p if ans is None else min(ans, p)

    if ans is not None:
      print('done:', n, g1)
      return ans

  assert False, 'did not find ans'

def part1() -> None:
  p = list(map(int, data))
  total = sum(p)
  print('packages:', len(p), total)
  print(solve(p, 3))

def part2() -> None:
  p = list(map(int, data))
  total = sum(p)
  print('packages:', len(p), total)
  print(solve(p, 4))

part2()
