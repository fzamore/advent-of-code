from collections import defaultdict

input = open('day12.txt').read().splitlines()

Registers = dict[str, int]

def resolve(registers: Registers, value: str) -> int:
  if value in ['a', 'b', 'c', 'd']:
    return registers[value]
  else:
    return int(value)

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
          pc += int(v[2])
          # Skip incrementing pc.
          continue
      case _:
        assert False, 'bad instr'
    pc += 1

def part1() -> None:
  instrs = input
  print('instrs:', len(instrs))
  r: Registers = defaultdict(int)
  execute(r, instrs)
  print(r['a'])

def part2() -> None:
  instrs = input
  print('instrs:', len(instrs))

  r = defaultdict(int)
  r['c'] = 1

  # Execute the first 9 instructions (this is a loop).
  execute(r, instrs[:9])
  print('registers:', r)

  # This is the second loop (simplified by hand, skipping updates to 'c'
  # and 'd', which aren't needed).
  for _ in range(r['d']):
    r['a'] += r['b']
    r['b'] = r['a'] - r['b']
  print('registers:', r)

  # The third loop adds 11 to 'a' 18 times.
  r['a'] += 11 * 18
  print('registers:', r)

  print(r['a'])

part2()
