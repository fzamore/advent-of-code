from common.ints import ints

data = open('day23.txt').read().splitlines()

Registers = dict[str, int]
Instr = str

def executeInstrs(r: Registers, instrs: list[Instr]) -> None:
  pc = 0
  while pc < len(instrs):
    instr = instrs[pc]
    v = instr.split()
    d = ints(instr)

    match v[0]:
      case 'hlf':
        assert len(d) == 0, 'not expecting ints in hlf instr'
        r[v[1]] //= 2
      case 'tpl':
        assert len(d) == 0, 'not expecting ints in tpl instr'
        r[v[1]] *= 3
      case 'inc':
        assert len(d) == 0, 'not inspecting ints in inc instr'
        r[v[1]] += 1
      case 'jmp':
        assert len(d) == 1, 'missing arg in jmp'
        pc += d[0]
        continue
      case 'jie':
        assert len(d) == 1, 'missing arg in jie'
        if r[v[1][:-1]] % 2 == 0:
          pc += d[0]
          continue
      case 'jio':
        assert len(d) == 1, 'missing arg in jio'
        if r[v[1][:-1]] == 1:
          pc += d[0]
          continue
      case _:
        assert False, 'bad instr'

    pc += 1

def part1() -> None:
  instrs = data
  print('len:', len(instrs))
  r = {'a': 0, 'b': 0}
  executeInstrs(r, instrs)
  print('done:', r)
  print(r['b'])

def part2() -> None:
  instrs = data
  print('len:', len(instrs))
  r = {'a': 1, 'b': 0}
  executeInstrs(r, instrs)
  print('done:', r)
  print(r['b'])

part2()
