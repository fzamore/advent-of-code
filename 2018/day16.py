from enum import Enum
from typing import Iterable

input = open('day16.txt').read().split("\n\n\n\n")

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

Registers = list[int]
Instr = list[int]
Group = tuple[Registers, Instr, Registers]

def parseList(l: str) -> list[int]:
  return list(map(int, l[1:-1].split(', ')))

def parseInput() -> tuple[list[Group], list[Instr]]:
  groups = []
  for groupS in input[0].split("\n\n"):
    group = groupS.splitlines()
    assert len(group) == 3
    groups.append((
      parseList(group[0].split(': ')[1]),
      list(map(int, group[1].split())),
      parseList(group[2].split(':  ')[1]),
    ))
  instrs = [list(map(int, l.split())) for l in input[1].splitlines()]
  return groups, instrs

def exec(op: Op, registers: Registers, instr: Instr) -> None:
  assert len(registers) == 4, 'invalid registers'
  assert len(instr) == 4, 'invalid instr'

  r = registers
  _, a, b, c = instr
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

def test(op: Op, group: Group) -> bool:
  before, instr, after = group
  r = before.copy()
  exec(op, r, instr)
  return all([r[i] == after[i] for i in range(4)])

def filterOpcodes(group: Group, opcodes: Iterable[Op]) -> list[Op]:
  return [op for op in opcodes if test(op, group)]

def part1() -> None:
  print()
  groups, _ = parseInput()
  print('groups:', len(groups))
  print(groups)

  c = 0
  for group in groups:
    ci = len(filterOpcodes(group, [o for o in Op]))
    print('ci:', ci)
    if ci >= 3:
      print('match:', group)
      c += 1
  print(c)

def part2() -> None:
  print()
  groups, instrs = parseInput()
  print('groups:', len(groups))

  remainingOpcodes = set([o for o in Op])
  map = {}
  while len(remainingOpcodes) > 0:
    for group in groups:
      possibleOpcodes = filterOpcodes(group, remainingOpcodes)
      if len(possibleOpcodes) == 1:
        matchedOpcode = group[1][0]
        print('match', matchedOpcode, possibleOpcodes[0])
        map[matchedOpcode] = possibleOpcodes[0]
        remainingOpcodes.remove(possibleOpcodes[0])

  assert len(map) == len([o for o in Op]), 'did not find all opcodes'
  print('map:', map)

  r = [0, 0, 0, 0]
  for instr in instrs:
    op = map[int(instr[0])]
    exec(op, r, instr)
  print(r[0])

part2()
