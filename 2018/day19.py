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

def part2() -> None:
  print()
  ir, instrs = parseInput()
  print('ir:', ir)
  print('instrs:', len(instrs))
  print('starting simulation...')

  # Solving this problem was a very manual process. Eventually, I figured
  # out that the program first computes a target number, and then stores
  # in r[0] the sum of all the prime factors of that number.

  r = [1, 0, 0, 0, 0, 0]

  # This is our target number (found by experimentation). It eventually
  # gets stored in r[2], and r[2] is never changed after that.
  target = 10551403 # prime factors: 1, 19, 555337, 10551403
  r[2] = target

  # During the process of finding the target, r0 gets reset to 0.
  r[0] = 0 # ip 34

  # Below is a simulation of my input, which some critical shortcuts. Only
  # r0, r3, and r5 will change. r2 is always set to the target. I skip
  # updating r1, since it's only used to modify the instruction pointer.
  # The outer loop increments r3 and the inner loop increments r5,
  # updating r0 if it's ever the case that r3 * r5 == r2.

  # These are the initial values of the registers once the two main loops get going:
  #   [0, 3, 10551403, 1, 0, 1]

  r[3] = 1 # ip 1
  # The outer loop, which updates r3.
  while r[3] <= r[2]: # ip 13
    r[5] = 1 # ip 2

    # This is a simplication of the commented-out inner loop below. In the
    # inner loop, r0 is updated if r3 * r5 == r2. This means we are
    # looking for the value of r5 such that r5 * r3 == r2. Since r2 never
    # changes, and since r3 doesn't change within each instance of the
    # inner loop, we can skip the inner loop altogether by checking
    # whether r3 divides r2, and if so, adding r3 to r0.
    if r[2] % r[3] == 0:
      print('updating r0:', r[0], r[3])
      r[0] += r[3] # ip 7

    # The commented-out inner loop.
    # while r[5] <= r[2]: # ip 9
    #   if r[3] * r[5] == r[2]: # ip 3,4
    #     r[0] += r[3] # ip 7
    #   r[5] += 1 # ip 8

    r[3] += 1 # ip 12

  print(r[0])

part2()
