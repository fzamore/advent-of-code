from enum import IntEnum

input = open('day13.txt').read().split(',')

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

def runMachine(memory: dict[int, int]) -> list[int]:
  outputs = []
  pc = 0
  relativeBase = 0
  ball = (-1, -1)
  paddle = -1
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
        # The only thing we need to do is keep the paddle under the ball.
        # We don't need to keep track of bricks.
        if ball[0] < paddle:
          joy = -1
        elif ball[0] > paddle:
          joy = 1
        else:
          joy = 0
        memory[dst] = joy
        pc += Op.getParamCount(opcode) + 1
      case Op.OUTPUT:
        pc += Op.getParamCount(opcode) + 1
        outputs.append(paramValues[0])
        if len(outputs) % 3 == 0:
          x, y, type = outputs[-3:]
          if x == -1 and y == 0:
            print('score:', type)
            continue
          match type:
            case 0: pass # empty
            case 1: pass # wall
            case 2: pass # block
            case 3: # paddle
              paddle = x
            case 4:
              ball = (x, y)
            case _:
              assert False, 'bad outputs'
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

  return outputs

def part1() -> None:
  memory = dict(zip(range(len(input)), list(map(int, input))))
  outputs = runMachine(memory)
  assert len(outputs) % 3 == 0, 'bad number of outputs'

  count = 0
  for i in range(0, len(outputs), 3):
    if outputs[i+2] == 2:
      count += 1
  print(count)

def part2() -> None:
  print()
  print('start:')
  memory = dict(zip(range(len(input)), list(map(int, input))))
  memory[0] = 2
  runMachine(memory)

part2()
