from collections import namedtuple
from typing import Optional
from common.ints import ints

input = open('day13.txt').read().splitlines()

Button = tuple[int, int]
Machine = namedtuple('Machine', ['a', 'b', 'prize'])

def parseInput(delta: int = 0) -> list[Machine]:
  machines = []
  i = 0
  while i < len(input):
    machines.append(Machine(
      tuple(ints(input[i])),
      tuple(ints(input[i + 1])),
      tuple([i + delta for i in ints(input[i + 2])]),
    ))
    i += 4
  return machines

def findMinTokens(machine: Machine) -> Optional[int]:
  # This is simple constant time algebra.
  #
  # Initial equations:
  #   a * ax + b * bx = px
  #   a * ay + b * by = py
  #
  # Solving for a and b:
  #   a = (px - b * bx) / ax
  #   b = (px - a * ax) / bx
  #
  # Substituting / solving for b:
  #   b = (px * ay - py * ax) / (bx * ay - by * ax)
  #
  # Everything is known except a and b.

  (ax, ay), (bx, by), (px, py) = machine

  # Solve for b.
  numerator = px * ay - py * ax
  denominator = bx * ay - by * ax
  assert denominator != 0, 'bad denominator'
  if numerator % denominator != 0:
    return None

  b = numerator // denominator

  # Use b to solve for a.
  numerator = px - b * bx
  if numerator % ax != 0:
    return None

  a = numerator // ax

  # Three tokens for a, one token for b.
  return a * 3 + b

def part1() -> None:
  machines = parseInput()
  print('machines:', len(machines))

  ans = sum([t for t in map(findMinTokens, machines) if t is not None])
  print(ans)

def part2() -> None:
  machines = parseInput(10000000000000)
  print('machines:', len(machines))

  ans = sum([t for t in map(findMinTokens, machines) if t is not None])
  print(ans)

part2()
