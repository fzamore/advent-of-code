from collections import defaultdict, namedtuple
from typing import Optional

input = open('day18.txt').read().splitlines()

Registers = dict[str, int]

class Program:
  registers: Registers
  pc: int
  queue: list[int]
  sound: int
  def __init__(self):
    self.registers = defaultdict(int)
    self.pc = 0
    self.queue = []
    self.sound = 0

Instr = namedtuple('Instr', ['cmd', 'args'])

def parseInput() -> list[Instr]:
  instrs = []
  for line in input:
    v = line.split()
    assert len(v) in [2,3], 'bad instr'
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
    result = registers[value]
    assert isinstance(result, int)
    return result
  return int(value)

def execInstr(program: Program, otherProgram: Program, instr: Instr) -> int:
  r = program.registers
  cmd, args = instr
  r1 = args[0]
  v1 = resolve(r, r1)

  r2 = args[1] if len(args) == 2 else None
  v2 = resolve(r, r2)

  match cmd:
    case 'snd':
      otherProgram.queue.append(v1)
      program.sound = v1
    case 'set':
      r[r1] = v2
    case 'add':
      r[r1] = v1 + v2
    case 'mul':
      r[r1] = v1 * v2
    case 'mod':
      r[r1] = v1 % v2
    case 'rcv':
      if len(program.queue) == 0:
        # Nothing to process.
        return 0
      r[r1] = program.queue.pop(0)
    case 'jgz':
      if v1 > 0:
        assert v2 != 0, 'cannot jump to same instruction'
        return v2
    case _:
      assert False, 'bad instr'

  # Offset to next instruction.
  return 1

def iterate(program: Program, otherProgram: Program, instrs: list[Instr]) -> tuple[bool, int]:
  isDone = True
  sends = 0
  while 0 <= program.pc < len(instrs):
    instr = instrs[program.pc]
    if instr[0] == 'snd':
      sends += 1
    offset = execInstr(program, otherProgram, instr)
    if offset == 0:
      # We tried to receive on an empty queue. Stop.
      break

    # We successfully executed at least one instruction, so we're not done.
    isDone = False
    program.pc += offset

  return isDone, sends

def part1() -> None:
  program = Program()

  instrs = parseInput()
  print('instrs:', len(instrs))

  while True:
    instr = instrs[program.pc]
    offset = execInstr(program, program, instr)
    program.pc += offset
    if instr[0] == 'rcv':
      print(program.sound)
      return

def part2() -> None:
  p0, p1 = Program(), Program()
  p0.registers['p'] = 0
  p1.registers['p'] = 1

  instrs = parseInput()
  print('instrs:', len(instrs))

  p1Sends = 0
  p0IsDone, p1IsDone = False, False
  while not (p0IsDone and p1IsDone):
    # Iterate each program independently until they're both done.
    p0IsDone, _ = iterate(p0, p1, instrs)
    p1IsDone, sends = iterate(p1, p0, instrs)
    p1Sends += sends

  print('done. programs:', p0.pc, p1.pc, p0.queue, p1.queue)
  print(p1Sends)

part2()
