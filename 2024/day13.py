from collections import namedtuple
from typing import Optional
from common.ints import ints

input = open('day13.txt').read().splitlines()

Button = tuple[int, int]
Machine = namedtuple('Machine', ['a', 'b', 'prize'])

def parseInput() -> list[Machine]:
  machines = []
  i = 0
  while i < len(input):
    machines.append(Machine(
      tuple(ints(input[i])),
      tuple(ints(input[i + 1])),
      tuple(ints(input[i + 2])),
    ))
    i += 4
  return machines

def findMinTokens(machine: Machine, n: int = 100) -> Optional[int]:
  # Equations:
  #   a * ax + b * bx = px
  #   a * ay + b * by = py
  (ax, ay), (bx, by), (px, py) = machine
  best = 10000
  foundAny = False
  for i in range(n):
    a = i
    # b = (px - a * ax) / bx
    numerator = px - a * ax
    if numerator % bx != 0:
      continue

    b = numerator // bx

    if a * ay + b * by != py:
      continue

    if a > 100 or b > 100:
      continue

    foundAny = True
    best = min(best, a * 3 + b)

  return best if foundAny else None

def part1() -> None:
  machines = parseInput()
  print('machines:', len(machines))

  ans = sum([t for t in map(findMinTokens, machines) if t is not None])
  print(ans)

part1()
