from typing import Optional
from common.ints import ints

input = open('day17.txt').read().splitlines()

def parseInput() -> tuple[int, int, int, list[int]]:
  a, b, c, instrs = None, None, None, None
  for line in input:
    if line == '':
      continue

    v = line.split(': ')
    if v[0] == 'Program':
      instrs = ints(line)
    elif v[0][-1] == 'A':
      a = int(v[1])
    elif v[0][-1] == 'B':
      b = int(v[1])
    elif v[0][-1] == 'C':
      c = int(v[1])
    else:
      assert False, 'bad input line: %s' % line

  assert a is not None and b is not None and c is not None and instrs is not None
  return a, b, c, instrs

def evalOperand(op: int, a: int, b: int, c: int) -> int:
  match op:
    case 0 | 1 | 2 | 3:
      return op
    case 4:
      return a
    case 5:
      return b
    case 6:
      return c
    case _:
      assert False, 'bad operand: %d' % op

def execInstr(a: int, b: int, c: int, ip: int, instrs: list[int]) -> tuple[int, int, int, int, Optional[int]]:
  def combo(op: int) -> int:
    return evalOperand(op, a, b, c)

  instr = instrs[ip]
  op = instrs[ip + 1]
  out = None
  match instr:
    case 0:
      a = a // (2 ** combo(op))
    case 1:
      b = b ^ op
    case 2:
      b = combo(op) % 8
    case 3:
      if a != 0:
        return a, b, c, op, out
    case 4:
      b = b ^ c
    case 5:
      out = combo(op) % 8
    case 6:
      b = a // (2 ** combo(op))
    case 7:
      c = a // (2 ** combo(op))
    case _:
      assert False, 'bad instr: %d' % instr

  return a, b, c, ip + 2, out

def part1() -> None:
  a, b, c, instrs = parseInput()
  print('input:', a, b, c, instrs)

  outputs = []
  ip = 0
  while 0 <= ip < len(instrs):
    a, b, c, ip, out = execInstr(a, b, c, ip, instrs)
    if out is not None:
      outputs.append(str(out))

  print(','.join(outputs))

part1()
