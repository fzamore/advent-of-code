from enum import IntEnum

input = open('day21.txt').read().split(',')

class Op(IntEnum):
  ADD: int = 1
  MUL: int = 2
  INPUT: int = 3
  OUTPUT: int = 4
  JUMP_IF_TRUE: int = 5
  JUMP_IF_FALSE: int = 6
  LESS_THAN: int = 7
  EQUALS: int = 8
  RELATIVE_BASE: int = 9

  @staticmethod
  def getParamCount(op: int) -> int:
    return {
      Op.ADD: 3,
      Op.MUL: 3,
      Op.INPUT: 1,
      Op.OUTPUT: 1,
      Op.JUMP_IF_TRUE: 2,
      Op.JUMP_IF_FALSE: 2,
      Op.LESS_THAN: 3,
      Op.EQUALS: 3,
      Op.RELATIVE_BASE: 1,
   }[Op(op)]

def getParameterAddresses(memory: dict[int, int], pc: int, relativeBase: int) -> list[int]:
  value = memory[pc]
  opcode = value % 100
  paramModes = str(value // 100)[::-1] + '000' # tack on extra zeroes, which is the default
  results = []
  for i in range(Op.getParamCount(opcode)):
    mode = paramModes[i]
    match mode:
      case '0':
        address = memory.get(pc + i + 1, 0)
      case '1':
        address = pc + i + 1
      case '2':
        address = memory.get(pc + i + 1, 0) + relativeBase
      case _:
        assert False, 'bad mode: %s' % mode
    results.append(address)
  assert len(results) <= 3, 'bad addresses: %s' % results
  return results

def runMachine(memory: dict[int, int], inputs: list[int]) -> None:
  pc = 0
  relativeBase = 0
  while (value := memory[pc]) != 99:
    opcode = value % 100
    paramAddresses = getParameterAddresses(memory, pc, relativeBase)
    paramValues = [memory.get(x, 0) for x in paramAddresses]
    assert len(paramValues) == Op.getParamCount(opcode), \
      'bad paramValues for opcode: %d, %s' % (opcode, paramValues)

    # Asssume the destination is the last parameter, if it exists.
    dst = paramAddresses[-1]
    assert dst >= 0, 'dst cannot be negative'

    match opcode:
      case Op.ADD:
        memory[dst] = paramValues[0] + paramValues[1]
        pc += Op.getParamCount(opcode) + 1
      case Op.MUL:
        memory[dst] = paramValues[0] * paramValues[1]
        pc += Op.getParamCount(opcode) + 1
      case Op.INPUT:
        assert dst >= 0, 'dst cannot be negative'
        memory[dst] = inputs.pop(0)
        pc += Op.getParamCount(opcode) + 1
      case Op.OUTPUT:
        o = paramValues[0]
        if o <= 0x7F:
          print(chr(o), end='')
        else:
          print(o)
        pc += Op.getParamCount(opcode) + 1
      case Op.JUMP_IF_TRUE:
        if paramValues[0] != 0:
          pc = paramValues[1]
        else:
          pc += Op.getParamCount(opcode) + 1
      case Op.JUMP_IF_FALSE:
        if paramValues[0] == 0:
          pc = paramValues[1]
        else:
          pc += Op.getParamCount(opcode) + 1
      case Op.LESS_THAN:
        memory[dst] = 1 if paramValues[0] < paramValues[1] else 0
        pc += Op.getParamCount(opcode) + 1
      case Op.EQUALS:
        memory[dst] = 1 if paramValues[0] == paramValues[1] else 0
        pc += Op.getParamCount(opcode) + 1
      case Op.RELATIVE_BASE:
        relativeBase += paramValues[0]
        pc += Op.getParamCount(opcode) + 1
      case _:
        assert False, 'bad opcode: %s' % opcode

def runAsciiProgram(program: list[str]) -> None:
  memory = dict(zip(range(len(input)), list(map(int, input))))

  inputs = []
  for inst in program:
    for c in inst:
      inputs.append(ord(c))
    inputs.append(ord('\n'))

  runMachine(memory, inputs)

def part1() -> None:
  # Jump if (1, 2, or 3 spaces ahead is a hole) AND (4 spaces ahead is ground).
  #  (~A v ~B v ~C) ^ D
  program = [
    'NOT A J',
    'NOT B T',
    'OR T J',
    'NOT C T',
    'OR T J',
    'AND D J',
    'WALK',
  ]
  runAsciiProgram(program)

def part2() -> None:
  # Break the program into the next two jumps, and jump if both jumps are
  # possible.
  #
  # The condition for the first jump is the same as part 1: whether there
  # is a hole in the next three spaces and four spaces ahead is a hole.
  #
  # The condition for the second jump is whether the fifth space ahead is
  # ground (i.e., we don't need to jump right away and can walk at least
  # one step forward) OR the condition for the first jump translated four
  # steps forward (i.e., if any of the 5, 6, 7 spaces is a hole AND the 8
  # space is ground). Note that we don't use the 9-space (register I) at
  # all.
  #
  # This results in the following boolean expression:
  #   (D ^ (~A v ~B v ~C)) ^ (E v (H ^ (~E v ~F v ~G)))
  #
  # To simplify the second half: (E v (H ^ (~E v ~F v ~G))), consider two
  # cases: E is true or E is false. If E is true, then the entire
  # expression is trivially true. If E is false, then (~E v ~F v ~G) is
  # true, so we can remove it from the expression, leaving:
  #   (D ^ (~A v ~B v ~C)) ^ (E v H)
  #
  # This is equivalent to: (D ^ ~(A ^ B ^ C)) ^ (E v H)
  #   (fewer NOT operations)
  program = [
    # (D ^ ~(A ^ B ^ C))
    'OR C T',
    'AND B T',
    'AND A T',
    'NOT T T',
    'AND D T',

    # (E v H)
    'OR E J',
    'OR H J',

    # Combining the two above expressions.
    'AND T J',

    'RUN',
  ]
  runAsciiProgram(program)

part2()
