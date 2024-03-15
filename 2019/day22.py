from collections import namedtuple
from enum import Enum

input = open('day22.txt').read().splitlines()

class Op(Enum):
  STACK = 1
  CUT = 2
  INCR = 3

Instr = namedtuple('Instr', ['op', 'value'])

def parseInput() -> list[Instr]:
  instrs: list[Instr] = []
  for line in input:
    if line.startswith('deal into new stack'):
      op, val = Op.STACK, -1
    elif line.startswith('cut'):
      op, val = Op.CUT, int(line.split()[-1])
    elif line.startswith('deal with increment'):
      op, val = Op.INCR, int(line.split()[-1])
      assert val > 0, 'incr value should be positive'
    else:
      assert False, 'bad input line: %s' % line

    instrs.append(Instr(op, val))
  return instrs

# Finds the coefficients of the function f(x) = ax + b, where x is an
# initial card (i.e., index), and the result of the function is the
# position of card x after all instructions are processed.
#
# Each instruction (stack, cut, or incr) modifies the index by a simple
# mathematical expression, modulo n. We track a and b such that (ax + b)
# is the desired expression.
def findCoefficients(instrs: list[Instr], n: int) -> tuple[int, int]:
  # Initially, we want (ax + b) to equal x, so we initialize a to 1 and b to 0.
  a, b = 1, 0
  for instr in instrs:
    match instr.op:
      case Op.STACK:
        # x1 = -x - 1
        # x1 = -(ax + b) - 1 = (-a)x + (-b - 1)
        a *= -1
        b = -b - 1
      case Op.CUT:
        # x1 = x - v
        # x1 = (ax + b) - v = (a)x + (b - v)
        b -= instr.value
      case Op.INCR:
        # x1 = x0 * v
        # x1 = (ax + b) * v = (va)x + (vb)
        a *= instr.value
        b *= instr.value
      case _:
        assert False, 'bad instruction'

    # Keep a and b modulo n.
    a %= n
    b %= n

  return a, b

def part1() -> None:
  n = 10007
  print('n:', n)

  instrs = parseInput()
  print('instrs:', len(instrs))

  card = 2019
  a, b = findCoefficients(instrs, n)
  print('coefficients:', a, b)
  print((a * card + b) % n)

def part2() -> None:
  n = 119315717514047
  k = 101741582076661
  print('n:', n)
  print('k:', k)

  instrs = parseInput()
  print('instrs:', len(instrs))

  a, b = findCoefficients(instrs, n)
  print('coefficients:', a, b)
  assert (a < n) and (b < n), 'bad coefficients'

  # f(x) = ax + b
  # f(f(x)) = (a^2)x + ab + b
  # f(f(f(x))) = (a^3)x + (a^2)b + ab + b
  # Thus:
  #   f^k(x) = (a^k)x + b(a^0 + a^1 + a^2 + ... + a^(k - 1))

  # Formula for the sum of a geometric series with exponents [0, k-1]:
  #   (a^k - 1) / (a - 1)
  # Since we're modulo n, use the modular inverse of (a - 1) instead of dividing by it:
  #   (a^k - 1) * (a - 1)^(-1)  (mod n)
  # Thus:
  #   f^k(x) = (a^k)x + b * (a^k - 1) * (a - 1)^(-1)  (mod n)
  # Solving for x:
  #   x = (f^k(x) - b * (a^k - 1) * (a - 1)^(-1)) * a^(-k)  (mod n)

  target = 2020
  k = 101741582076661
  asum = (pow(a, k, n) - 1) * pow(a - 1, -1, n)
  print(((target - b * asum) * pow(a, -k, n)) % n)

part2()
