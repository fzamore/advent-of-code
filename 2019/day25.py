from enum import IntEnum
from typing import Optional

inp = open('day25.txt').read().split(',')

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

def runMachine(
  memory: dict[int, int],
  inputs: list[int],
  pc: int,
  relativeBase: int,
) -> Optional[tuple[int, int]]:
  while (value := memory[pc]) != 99:
    opcode = value % 100
    paramAddresses = getParameterAddresses(memory, pc, relativeBase)
    paramValues = [memory.get(x, 0) for x in paramAddresses]
    assert len(paramValues) == Op.getParamCount(opcode), \
      'bad paramValues for opcode: %d, %s' % (opcode, paramValues)

    # Asssume the destination is the last parameter, if it exists.
    dst = paramAddresses[-1]
    assert dst >= 0, 'dst cannot be negative: %d' % dst

    match opcode:
      case Op.ADD:
        memory[dst] = paramValues[0] + paramValues[1]
        pc += Op.getParamCount(opcode) + 1
      case Op.MUL:
        memory[dst] = paramValues[0] * paramValues[1]
        pc += Op.getParamCount(opcode) + 1
      case Op.INPUT:
        assert dst >= 0, 'dst cannot be negative'
        if len(inputs) == 0:
          return pc, relativeBase
        memory[dst] = inputs.pop(0)
        pc += Op.getParamCount(opcode) + 1
      case Op.OUTPUT:
        o = paramValues[0]
        print(chr(o), end='')
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

  return None

def convertToAsciiInputs(command: str) -> list[int]:
  if command == '':
    return []
  inputs = []
  for c in command:
    inputs.append(ord(c))
  inputs.append(ord('\n'))
  return inputs

def part1() -> None:
  memory = dict(zip(range(len(inp)), list(map(int, inp))))
  pc, relativeBase = 0, 0
  inputs: list[int] = []

  # I got pretty lucky when exploring the maze manually and drawing out
  # the maze on paper. I manually determined the correct combination of
  # items I needed to get past the checkpoint: mug, prime number, food
  # ration, and fuel cell.

  # Through manual exploration, I found the following sequence of commmands.
  commands = [
    'east',
    'take food ration',
    'south',
    'take prime number',
    'north',
    'east',
    'east',
    'north',
    'north',
    'take fuel cell',
    'south',
    'south',
    'west',
    'west',
    'west',
    'north',
    'north',
    'west',
    'take mug',
    'east',
    'south',
    'west',
    'north',
    'west',
    'north',
  ]

  while True:
    result = runMachine(memory, inputs, pc, relativeBase)
    if result is None:
      break
    pc, relativeBase = result
    if len(commands) > 0:
      command = commands.pop(0)
    else:
      command = input('--> ')
    inputs = convertToAsciiInputs(command)

part1()
