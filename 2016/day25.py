from collections import defaultdict
from math import prod

data = open('day25.txt').read().splitlines()

Registers = dict[str, int]

def resolve(registers: Registers, value: str) -> int:
  if value in ['a', 'b', 'c', 'd']:
    return registers[value]
  else:
    return int(value)

def execute(r: Registers, instrs: list[str], n: int) -> list[int]:
  outputs = []
  pc = 0
  while 0 <= pc < len(instrs):
    instr = instrs[pc]
    v = instr.split()
    match v[0]:
      case 'cpy':
        r[v[2]] = resolve(r, v[1])
      case 'inc':
        r[v[1]] += 1
      case 'dec':
        r[v[1]] -= 1
      case 'jnz':
        if resolve(r, v[1]) != 0:
          pc += int(v[2])
          # Skip incrementing pc.
          continue
      case 'out':
        outv = resolve(r, v[1])
        outputs.append(outv)
        if len(outputs) == n:
          return outputs
      case _:
        assert False, 'bad instr'
    pc += 1
  return outputs

# Finds the smallest integer at least n that when divided by two produces
# an alternating sequence of even and odd numbers. It works by starting
# with zero (even), and then either doubling or doubling + 1 to produce
# alternating evens and odds.
def findAlternatingIntegerAtLeast(n: int) -> int:
  result = 0
  i = 0
  while True:
    if result >= n:
      return result
    result *= 2
    if i % 2 == 1:
      result += 1
    i += 1

def part1() -> None:
  instrs = data
  print('instrs:', len(instrs))

  # Through inspection and testing, the sequence of instructions works
  # as follows. The input "a" is increased by a constant. Then, there
  # is a loop which outputs 0 if "a" is even (or 1 is "a" is
  # odd). Next, it divides "a" by 2 and repeats. When "a" gets to
  # zero, it is reset to the value of the original value (with the
  # constant added) and the process repeats.
  #
  # So, we need the value of (a + k) to be the smallest integer such that
  # repeatedly dividing by two produces an alternating sequence of even
  # and odd numbers.

  # The constant can be derived from instructions at known indicies.
  k = prod([int(instrs[i].split()[1]) for i in [1, 2]])
  print('k:', k)

  ak = findAlternatingIntegerAtLeast(k)
  print('a + k:', ak)

  a = ak - k
  print('trying:', a)

  # Execute until we have 100 output instructions to verify we guessed correctly.
  n = 100
  r = defaultdict(int)
  r['a'] = a
  outputs = execute(r, instrs, n)
  assert len(outputs) == n, 'wrong number of outputs'
  print('output sequence:', outputs)
  for i, v in enumerate(outputs):
    assert v == i % 2, 'non-alternating output sequence'

  print(a)

part1()
