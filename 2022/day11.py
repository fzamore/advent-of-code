from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

input = open('day11.txt').read().split("\n\n")

class Operator(Enum):
  MUL = 1
  ADD = 2

@dataclass
class Monkey:
  id: int
  items: list[int]
  operator: Operator
  operand: int | str # either an int or "old"
  mod: int
  dst: tuple[int, int] # if true: dst[0], else: dst[1]

def parseMonkey(m: str) -> Monkey:
  id = int(m[0].split()[1][:-1])
  items = list(map(int, m[1].split(':')[1].split(',')))
  operator = Operator.MUL if m[2].split(' old ')[1][0] == '*' else Operator.ADD
  operand: int | str = m[2].split()[-1]
  if operand != 'old':
    operand = int(operand)
  mod = int(m[3].split(' by ')[1])
  dst = (
    int(m[4].split(' monkey ')[1]),
    int(m[5].split(' monkey ')[1]),
  )
  return Monkey(id, items, operator, operand, mod, dst)

def takeTurn(monkeys: dict[int, Monkey], monkeyid: int) -> int:
  count = 0
  monkey = monkeys[monkeyid]
  while len(monkey.items) > 0:
    item = monkey.items.pop(0)
    count += 1
    operand2 = int(item if monkey.operand == 'old' else monkey.operand)
    if monkey.operator == Operator.ADD:
      item += operand2
    else:
      item *= operand2
    item //= 3
    dstid = monkey.dst[0] if item % monkey.mod == 0 else monkey.dst[1]
    monkeys[dstid].items.append(item)
  return count

def doRound(monkeys: dict[int, Monkey]) -> dict[int, int]:
  counts = {}
  for i in range(len(monkeys)):
    counts[i] = takeTurn(monkeys, i)
  return counts

def part1():
  monkeys = {}
  for m in input:
    monkey = parseMonkey(m.splitlines())
    monkeys[monkey.id] = monkey
  print(monkeys)
  print('monkey count', len(monkeys))

  allCounts = defaultdict(int)
  for _ in range(20):
    counts = doRound(monkeys)
    for i in counts:
      allCounts[i] += counts[i]
  print(monkeys)
  print(allCounts)
  s = sorted(allCounts.values(), reverse=True)
  print(s[0] * s[1])

part1()
