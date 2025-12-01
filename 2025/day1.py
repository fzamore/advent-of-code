from typing import Iterable

data = open('day1.txt').read().splitlines()

def parse() -> Iterable[int]:
  for line in data:
    r = -1 if line[0] == 'L' else 1
    yield r * int(line[1:])

def part1() -> None:
  dial = 50
  m = 100
  ans = 0
  for v in parse():
    dial = (dial + v) % m
    if dial == 0:
      ans += 1
  print(ans)

def part2() -> None:
  dial = 50
  m = 100
  ans = 0
  for v in parse():
    # Full loops.
    ans += abs(v) // m

    newdial = (dial + v) % m
    if dial != 0:
      # Special-case zero, and don't double-count it.
      if newdial == 0:
        ans += 1
      # Partial loop going right.
      elif v > 0 and newdial < dial:
        ans += 1
      # Partial loop going left.
      elif v < 0 and newdial > dial:
        ans += 1
    dial = newdial
  print(ans)

part2()
