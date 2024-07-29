from enum import Enum
from typing import Optional

input = open('day21.txt').read().splitlines()

class Op(Enum):
  ADDR = 1
  ADDI = 2
  MULR = 3
  MULI = 4
  BANR = 5
  BANI = 6
  BORR = 7
  BORI = 8
  SETR = 9
  SETI = 10
  GTIR = 11
  GTRI = 12
  GTRR = 13
  EQIR = 14
  EQRI = 15
  EQRR = 16

Registers = list[int] # Always length 6
Instr = tuple[Op, int, int, int]

def exec(registers: Registers, instr: Instr) -> None:
  r = registers
  op, a, b, c = instr
  match op:
    case Op.ADDR:
      r[c] = r[a] + r[b]
    case Op.ADDI:
      r[c] = r[a] + b
    case Op.MULR:
      r[c] = r[a] * r[b]
    case Op.MULI:
      r[c] = r[a] * b
    case Op.BANR:
      r[c] = r[a] & r[b]
    case Op.BANI:
      r[c] = r[a] & b
    case Op.BORR:
      r[c] = r[a] | r[b]
    case Op.BORI:
      r[c] = r[a] | b
    case Op.SETR:
      r[c] = r[a]
    case Op.SETI:
      r[c] = a
    case Op.GTIR:
      r[c] = int(a > r[b])
    case Op.GTRI:
      r[c] = int(r[a] > b)
    case Op.GTRR:
      r[c] = int(r[a] > r[b])
    case Op.EQIR:
      r[c] = int(a == r[b])
    case Op.EQRI:
      r[c] = int(r[a] == b)
    case Op.EQRR:
      r[c] = int(r[a] == r[b])
    case _:
      assert False, 'bad op'

# Executes the given program and returns the value of r0 which first
# causes the program to halt.
def execAll(r: Registers, ir: int, instrs: list[Instr]) -> int:
  i = 0
  while r[ir] >= 0 and r[ir] < len(instrs):
    instr = instrs[r[ir]]

    if i % 100000 == 0:
      print('exec:', i, r[ir], r)

    # This instruction halts the program if r[2] == r[0], so r[2] is what
    # we're looking for.
    if r[ir] == 28:
      print('checking against r0:', i, r[2], r)
      return r[2]

    exec(r, instr)
    r[ir] += 1
    i += 1
  return i

def parseInput() -> tuple[int, list[Instr]]:
  # Mapping of lowercase op names to Op.
  d = dict([(o.name.lower(), o) for o in Op])

  assert input[0].split()[0] == '#ip'
  ir = int(input[0].split()[1])
  instrs = []
  for line in input[1:]:
    v = line.split()
    assert len(v) == 4, 'bad input line'
    op = d[v[0]]
    operands = tuple(map(int, v[1:]))
    assert len(operands) == 3, 'bad input line'
    instrs.append((op,) + operands)

  return ir, instrs

def part1() -> None:
  ir, instrs = parseInput()
  print('ir:', ir)
  print('instrs:', len(instrs))

  registers = [0, 0, 0, 0, 0, 0]
  print(execAll(registers, ir, instrs))

part1()
