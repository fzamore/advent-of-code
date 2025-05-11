from collections import defaultdict
from math import factorial, prod

data = open('day23.txt').read().splitlines()

Registers = dict[str, int]

def resolve(registers: Registers, value: str) -> int:
  if value in ['a', 'b', 'c', 'd']:
    return registers[value]
  else:
    return int(value)

def toggle(instrs: list[str], pc: int) -> None:
  if pc < 0 or pc >= len(instrs):
    print('skipping tgl:', pc)
    return

  instr = instrs[pc]
  v = instr.split()
  print('toggling:', pc, instr)
  match v[0]:
    case 'cpy':
      dst = 'jnz'
    case 'jnz':
      dst = 'cpy'
    case 'inc':
      dst = 'dec'
    case 'dec' | 'tgl':
      dst = 'inc'
    case _:
      assert False, 'bad instr in toggle'

  instrs[pc] = ' '.join([dst] + v[1:])

def execute(r: Registers, instrs: list[str]) -> None:
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
          pc += resolve(r, v[2])
          # Skip incrementing pc.
          continue
      case 'tgl':
        offset = resolve(r, v[1])
        print('tgl:', pc, offset, r['a'])
        toggle(instrs, pc + offset)
      case _:
        assert False, 'bad instr: %s' % instr

    pc += 1

def part1() -> None:
  instrs = data
  print('instrs:', len(instrs))
  r: Registers = defaultdict(int)
  r['a'] = 7
  execute(r, instrs)
  print(r['a'])

def part2() -> None:
  # This solution was based on a combination of inspection and testing,
  # and may not work for other inputs.
  #
  # There is a single "tgl" instruction in the input. Whenever we hit that
  # instruction, the value of "a" is the next value in its factorial.
  # E.g., if "a" is initialized to 12, "a" becomes 132 (12 * 11), then
  # 1320 (12 * 11 * 10), then 11880 (12 * 11 * 10 * 9), etc.
  #
  # The "tgl" instruction is a no-op until the final four times it is
  # executed. In those four times, it toggles offset 8, 4, 6, and 2
  # respectively. The final time the "tgl" is executed (offset 2) is what
  # allows the program to continue past a "jnz" instruction (because this
  # "jnz" is replaced with a "cpy"), and at that point, "a" is incremented
  # by a constant value, and the program terminates.
  #
  # So, the final value of "a" is: `a! + k`.

  instrs = data
  print('instrs:', len(instrs))

  # The constant can be derived from instructions at known indicies.
  k = prod([int(instrs[i].split()[1]) for i in [19, 20]])
  print('k:', k)

  print(factorial(12) + k)

part2()
