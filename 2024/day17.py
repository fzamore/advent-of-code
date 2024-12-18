from typing import Optional
from common.ints import ints

input = open('day17.txt').read().splitlines()

def parseInput() -> tuple[int, int, int, list[int]]:
  a, b, c, instrs = None, None, None, None
  for line in input:
    if line == '':
      continue

    v = line.split(': ')
    if v[0] == 'Program':
      instrs = ints(line)
    elif v[0][-1] == 'A':
      a = int(v[1])
    elif v[0][-1] == 'B':
      b = int(v[1])
    elif v[0][-1] == 'C':
      c = int(v[1])
    else:
      assert False, 'bad input line: %s' % line

  assert a is not None and b is not None and c is not None and instrs is not None
  return a, b, c, instrs

def evalOperand(op: int, a: int, b: int, c: int) -> int:
  match op:
    case 0 | 1 | 2 | 3:
      return op
    case 4:
      return a
    case 5:
      return b
    case 6:
      return c
    case _:
      assert False, 'bad operand: %d' % op

def execInstr(a: int, b: int, c: int, ip: int, instrs: list[int]) -> tuple[int, int, int, int, Optional[int]]:
  def combo(op: int) -> int:
    return evalOperand(op, a, b, c)

  instr = instrs[ip]
  op = instrs[ip + 1]
  out = None
  match instr:
    case 0:
      a = a // (2 ** combo(op))
    case 1:
      b = b ^ op
    case 2:
      b = combo(op) % 8
    case 3:
      if a != 0:
        return a, b, c, op, out
    case 4:
      b = b ^ c
    case 5:
      out = combo(op) % 8
    case 6:
      b = a // (2 ** combo(op))
    case 7:
      c = a // (2 ** combo(op))
    case _:
      assert False, 'bad instr: %d' % instr

  return a, b, c, ip + 2, out

def execProgram(a: int, b: int, c: int, instrs: list[int]) -> list[int]:
  outputs = []
  ip = 0
  while 0 <= ip < len(instrs):
    a, b, c, ip, out = execInstr(a, b, c, ip, instrs)
    if out is not None:
      outputs.append(out)
  return outputs

# This function returns the value output by the program, given an input to
# register A. This is based on manual analysis of my specific program
# input.
def computeOutput(a: int) -> int:
  return (a ^ (a // 2 ** ((a % 8) ^ 7))) % 8

# This function starts with the rightmost (smallest) value, and builds up
# until we have enough digits to satisfy the program.
def findValue(level: int, value: int, program: list[int]) -> Optional[int]:
  # Our target digit.
  target = program[len(program) - (level + 1)]
  assert 0 <= target < 8, 'bad target in program'

  # Through manual analysis, I determined that the input program does this:
  #
  #   do {
  #     B = mathematicalExpression(A)
  #     output(B)
  #     A = intdiv(A, 8)
  #   } while (A != 0)
  #
  # Thus, the program outputs exactly one octal digit per loop iteration.
  # Since the program terminates when A == 0, A must be [1, 7] during the
  # previous iteration of the loop. I derived how to compute B from A, so
  # we test all values [0, 7] of A and for each of them that results in B,
  # we have a candidate for that "level" of A. For each such candidate X,
  # we test the next level by testing the values [8 * X, 8 * X + 7] (since
  # that is the inverse of intdiv(8)). We continue this process until we
  # have enough digits as are in the input program, and then we have our
  # value of A.

  # Since the program uses intdiv by 8, there are 8 possible values that
  # could possibly result in the target.
  for test in range(value, value + 8):
    if computeOutput(test) == target:
      print('match for level:', level, test)

      if level == len(program) - 1:
        # Huzzah! We have our final answer.
        return test

      # Each output cycle of the program does intdiv by 8, so we multiply
      # by 8 and recur.
      if (result := findValue(level + 1, test * 8, program)) is not None:
        return result

  # This branch was a dead-end
  return None

def part1() -> None:
  a, b, c, instrs = parseInput()
  print('input:', a, b, c, instrs)

  outputs = execProgram(a, b, c, instrs)
  print(','.join([str(o) for o in outputs]))

def part2() -> None:
  _, b, c, instrs = parseInput()
  print('program:', instrs)

  ans = findValue(0, 0, instrs)
  assert ans is not None, 'did not find answer'
  assert execProgram(ans, b, c, instrs) == instrs, 'found incorrect answer'
  print(ans)

part2()
