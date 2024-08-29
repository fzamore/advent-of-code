from collections import Counter, namedtuple

input = open('day8.txt').read().splitlines()

Instr = namedtuple('Instr', [
  'dst',
  'value',
  'src',
  'cmpOp',
  'cmpValue',
])

def parseLine(line: str) -> Instr:
  v = line.split()
  assert len(v) == 7
  dst, command, valueS, _, src, cmpOp, cmpValue = v
  assert command in ['inc', 'dec']
  value = int(valueS) if command == 'inc' else -int(valueS)
  return Instr(dst, value, src, cmpOp, int(cmpValue))

def matchCmp(leftValue: int, cmpOp: str, rightValue: int) -> bool:
  match cmpOp:
    case '<':
      return leftValue < rightValue
    case '>':
      return leftValue > rightValue
    case '<=':
      return leftValue <= rightValue
    case '>=':
      return leftValue >= rightValue
    case '==':
      return leftValue == rightValue
    case '!=':
      return leftValue != rightValue
    case _:
      assert False, 'bad op: %s' % cmpOp

def part1() -> None:
  instrs = [parseLine(line) for line in input]

  registers: dict[str, int] = Counter()
  for instr in instrs:
    dst, value, src, cmpOp, cmpValue = instr
    if matchCmp(registers[src], cmpOp, cmpValue):
      registers[dst] += value

  print(max(registers.values()))

def part2() -> None:
  instrs = [parseLine(line) for line in input]

  registers: dict[str, int] = Counter()
  mx = 0
  for instr in instrs:
    dst, value, src, cmpOp, cmpValue = instr
    if matchCmp(registers[src], cmpOp, cmpValue):
      registers[dst] += value
      mx = max(registers[dst], mx)

  print(mx)

part2()
