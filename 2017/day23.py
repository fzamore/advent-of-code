from collections import defaultdict
from math import sqrt

input = open('day23.txt').read().splitlines()

Instr = tuple[str, str, str]
Registers = dict[str, int]

def isRegister(value: str) -> bool:
  if len(value) > 1:
    return False
  return ord('a') <= ord(value) <= ord('z')

def parseInstr(s: str) -> Instr:
  v = s.split()
  return v[0], v[1], v[2]

def parseInput() -> list[Instr]:
  return [parseInstr(l) for l in input]

def resolve(registers: Registers, value: str) -> int:
  if isRegister(value):
    result = registers[value]
    assert isinstance(result, int), 'registers must contain ints'
    return result
  return int(value)

def execInstr(registers, instr) -> int:
  r = registers
  cmd, r1, r2 = instr
  v1 = resolve(r, r1)
  v2 = resolve(r, r2)

  match cmd:
    case 'set':
      r[r1] = v2
    case 'sub':
      r[r1] -= v2
    case 'mul':
      r[r1] *= v2
    case 'jnz':
      if v1 != 0:
        assert v2 != 0, 'cannot jump to same instruction'
        return v2
    case _:
      assert False, 'bad instr'

  # Offset to next instruction.
  return 1

def isComposite(n: int) -> bool:
  for i in range(2, int(sqrt(n)) + 1):
    if n % i == 0:
      return True
  return False

def part1() -> None:
  instrs = parseInput()
  print('instrs:', len(instrs))

  pc = 0
  registers: Registers = defaultdict(int)

  ans = 0
  while 0 <= pc < len(instrs):
    instr = instrs[pc]
    if instr[0] == 'mul':
      ans += 1
    pc += execInstr(registers, instr)
  print(ans)

def part2() -> None:
  instrs = parseInput()
  print('instrs:', len(instrs))

  # This is a simplified / optimized version of the input assembly based
  # on manual analysis.
  #
  # The program halts when b == e, b == d, and b == c. b is initialized to
  # 108400 and c is initialized to 125400 (b + 17000). c never changes
  # after it is set. b is incremented by 1 in the outer loop, which halts
  # when b == c. f is always either 1 or 0. h gets incremented when f ==
  # 0, which occurs when e * d == b. That is the only time that h is
  # modified. There are two inner loops that increment d and e; the result
  # is that f is set to 0 (and thus h is incremented) if b is a composite
  # number.

  h = 0
  b = 108400
  c = 125400
  while True:
    if isComposite(b):
      # If b is composite, increment h.
      h += 1
    if b == c:
      break
    b += 17

  print(h)

part2()
