from enum import Enum

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

def manualIterate(r: Registers) -> int:
  seen: set[int] = set()
  lastChecked = None

  while True: # ip 28 loop
    r[1] = r[2] | 65536 # ip 6 (2^16 == 1, then 16 0's)
    r[2] = 1250634 # ip 7

    while True: # ip 13 loop
      r[2] = 16777215 & (65899 * (16777215 & (r[2] + (r[1] & 255)))) # ip 8, 9, 10, 11, 12

      if 256 > r[1]: # ip 13
        break

      r[4] = 0 # ip 17

      # while (r[4] + 1) * 256 <= r[1]: # ip 18, 19, 20; loop: [18,19,20,21,22,24,25]
      #   r[4] += 1 # ip 24
      # r[1] = r[4] # ip 26

      # The commented-out loop above can be simplified to this.
      r[1] //= 256

    if r[2] in seen:
      # We assume that once we've encountered a value we've already seen,
      # we will see no new values. Thus, the last value we saw before the
      # duplicate is the value that took the longest to find. Note that we
      # never read from r[0] when doing manual iteration.
      print('already seen:', r[2])
      assert lastChecked is not None, 'should have already checked a value'
      return lastChecked
    seen.add(r[2])
    lastChecked = r[2]

    # This bit halts the program, but we don't actually want the program
    # to halt (because we want to keep track of every value we ultimately
    # compare against r0 in this spot).
    # if r[2] == r[0]: # ip 28
    #   break

def part1() -> None:
  ir, instrs = parseInput()
  print('ir:', ir)
  print('instrs:', len(instrs))

  registers = [0, 0, 0, 0, 0, 0]
  print(execAll(registers, ir, instrs))

def part2() -> None:
  ir, instrs = parseInput()
  print('ir:', ir)
  print('instrs:', len(instrs))

  registers = [0, 0, 0, 0, 0, 0]
  print(manualIterate(registers))

part2()
