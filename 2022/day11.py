from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from math import prod
from typing import Optional

input = open('day11.txt').read().split("\n\n")

class Operator(Enum):
  MUL = 1
  ADD = 2
  SQUARE = 3

@dataclass
class Monkey:
  id: int
  items: list[int]
  operator: Operator
  operand: int
  mod: int
  dst: tuple[int, int] # if true: dst[0], else: dst[1]

def parseMonkey(m: list[str]) -> Monkey:
  id = int(m[0].split()[1][:-1])
  items = list(map(int, m[1].split(':')[1].split(',')))
  operator = Operator.MUL if m[2].split(' old ')[1][0] == '*' else Operator.ADD
  operand_str = m[2].split()[-1]
  if operand_str == 'old':
    # assume that if the operand is ever "old", it's "old * old"
    assert operator == Operator.MUL, 'invalid monkey: %s' % m
    operator = Operator.SQUARE
    operand = 0 # never used
  else:
    operand = int(operand_str)
  mod = int(m[3].split(' by ')[1])
  dst = (
    int(m[4].split(' monkey ')[1]),
    int(m[5].split(' monkey ')[1]),
  )
  return Monkey(id, items, operator, operand, mod, dst)

def parseMonkeys(input: list[str]) -> dict[int, Monkey]:
  monkeys = {}
  for m in input:
    monkey = parseMonkey(m.splitlines())
    monkeys[monkey.id] = monkey
  return monkeys

def takeTurn(
  monkeys: dict[int, Monkey],
  monkeyid: int,
  divisor: Optional[int],
) -> int:
  count = 0
  monkey = monkeys[monkeyid]
  while len(monkey.items) > 0:
    item = monkey.items.pop(0)
    count += 1
    match monkey.operator:
      case Operator.ADD: item += monkey.operand
      case Operator.MUL: item *= monkey.operand
      case Operator.SQUARE: item *= item
    if divisor is None:
      # For Part 1, we have no divisor, and instead do integer division by
      # three.
      item //= 3
    else:
      # In Part 2, we use a divisor (the product of all moduli) to keep
      # the numbers from getting too big.
      item %= divisor
    dstid = monkey.dst[0] if item % monkey.mod == 0 else monkey.dst[1]
    monkeys[dstid].items.append(item)
  return count

def doRound(
  monkeys: dict[int, Monkey],
  divisor: Optional[int],
) -> dict[int, int]:
  counts = {}
  for i in range(len(monkeys)):
    counts[i] = takeTurn(monkeys, i, divisor)
  return counts

def doAllRounds(
  round: int,
  monkeys: dict[int, Monkey],
  divisor: Optional[int] = None,
) -> dict[int, int]:
  allCounts: dict[int, int] = defaultdict(int)
  for _ in range(round):
    counts = doRound(monkeys, divisor)
    for i in counts:
      allCounts[i] += counts[i]
  return allCounts

def part1():
  monkeys = parseMonkeys(input)
  print('monkey count', len(monkeys))

  allCounts = doAllRounds(20, monkeys)
  print(allCounts)
  s = sorted(allCounts.values(), reverse=True)
  print(s[0] * s[1])

def part2():
  monkeys = parseMonkeys(input)
  divisor = prod([m.mod for m in monkeys.values()])
  print('monkey count', len(monkeys))
  print('divisor', divisor)

  allCounts = doAllRounds(10000, monkeys, divisor)
  print(allCounts)
  s = sorted(allCounts.values(), reverse=True)
  print(s[0] * s[1])

part2()
