from collections import namedtuple
from enum import Enum

input = open('day22.txt').read().splitlines()

class Op(Enum):
  STACK = 1
  CUT = 2
  INCR = 3

Instr = namedtuple('Instr', ['op', 'value'])

def parseInput() -> list[Instr]:
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

    instrs.append(Instr(op, val))
  return instrs

def part1() -> None:
  n = 10007
  print('n:', n)

  instrs = parseInput()
  print('instrs:', len(instrs))

  cardI = 2019
  for instr in instrs:
    match instr.op:
      case Op.STACK:
        cardI = n - 1 - cardI
      case Op.CUT:
        cardI = cardI - instr.value
      case Op.INCR:
        cardI = cardI * instr.value
      case _:
        assert False, 'bad instruction'
    cardI = cardI % n

  print(cardI)

part1()
