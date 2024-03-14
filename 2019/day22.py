from collections import namedtuple
from enum import Enum

input = open('day22.txt').read().splitlines()

class Op(Enum):
  STACK = 1
  CUT = 2
  INCR = 3

Instr = namedtuple('Instr', ['op', 'value'])

def stack(cards: list[int]) -> list[int]:
  return cards[::-1]

def cut(cards: list[int], val: int) -> list[int]:
  assert val != 0, 'cannot cut by 0'
  # Python does the right thing with negatives.
  return cards[val:] + cards[:val]

def incr(cards: list[int], val: int) -> list[int]:
  n = len(cards)
  result = [9999999] * n
  ri = 0
  for i in range(n):
    result[ri] = cards[i]
    ri = (ri + val) % n
  assert cards[0] == result[0], 'first card of incr should not change'
  return result

def part1() -> None:
  n = 10007
  print('n:', n)

  instrs: list[Instr] = []
  for line in input:
    if line.startswith('deal into new stack'):
      op, val = Op.STACK, -1
    elif line.startswith('cut'):
      op, val = Op.CUT, int(line.split()[-1])
    elif line.startswith('deal with increment'):
      op, val = Op.INCR, int(line.split()[-1])
      assert val > 0, 'incr value should be positive'
    else:
      assert False, 'bad input line: %s' % line
    assert abs(val) < n, 'bad value param: %d' % val

    instrs.append(Instr(op, val))

  print('instrs:', len(instrs))

  cards = list(range(n))

  for instr in instrs:
    match instr.op:
      case Op.STACK:
        cards = stack(cards)
      case Op.CUT:
        cards = cut(cards, instr.value)
      case Op.INCR:
        cards = incr(cards, instr.value)
      case _:
        assert False, 'bad instr'

    assert set(cards) == set(range(n)), 'card values are not correct'

  print(cards.index(2019))

part1()
