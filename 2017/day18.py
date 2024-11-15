from collections import defaultdict, namedtuple
from typing import Optional

input = open('day18.txt').read().splitlines()

Registers = dict[str, int]
Instr = namedtuple('Instr', ['cmd', 'args'])

def parseInput() -> list[Instr]:
  instrs = []
  for line in input:
    v = line.split()
    assert len(v) in [2,3]
    cmd = v[0]
    args = v[1:]
    instrs.append(Instr(cmd, args))
  return instrs

def isRegister(value: str) -> bool:
  if len(value) > 1:
    return False
  return ord('a') <= ord(value) <= ord('z')

def resolve(registers: Registers, value: Optional[str]) -> int:
  if value is None:
    return 0
  if isRegister(value):
    return registers[value]
  return int(value)

def execInstr(registers: Registers, instr: Instr) -> int:
  r = registers
  cmd, args = instr
  r1 = args[0]
  v1 = resolve(r, r1)

  r2 = args[1] if len(args) == 2 else None
  v2 = resolve(r, r2)

  match cmd:
    case 'snd':
      r['snd'] = v1
    case 'set':
      r[r1] = v2
    case 'add':
      r[r1] = v1 + v2
    case 'mul':
      r[r1] = v1 * v2
    case 'mod':
      r[r1] = v1 % v2
    case 'rcv':
      if r['snd'] != 0:
        r['rcv'] = r['snd']
    case 'jgz':
      if v1 > 0:
        return v2
    case _:
      assert False, 'bad instr'

  # Offset to next instruction.
  return 1

def part1() -> None:
  registers = defaultdict(int)
  registers['snd'] = 0

  instrs = parseInput()
  print('instrs:', len(instrs))

  pc = 0
  while True:
    offset = execInstr(registers, instrs[pc])
    pc += offset
    if registers['rcv'] != 0:
      print(registers['rcv'])
      return

part1()
