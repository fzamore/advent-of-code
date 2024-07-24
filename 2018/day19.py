from enum import Enum

input = open('day19.txt').read().splitlines()

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

def execAll(registers: Registers, ir: int, instrs: list[Instr]) -> None:
  r = registers
  ip = 0

  while ip >= 0 and ip < len(instrs):
    instr = instrs[ip]
    r[ir] = ip
    exec(r, instr)
    ip = r[ir]
    ip += 1

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
  print()
  ir, instrs = parseInput()
  print('ir:', ir)
  print('instrs:', len(instrs))

  registers = [0, 0, 0, 0, 0, 0]
  execAll(registers, ir, instrs)
  print('after finishing exec:', registers)
  print(registers[0])

part1()
