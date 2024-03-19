from collections import deque
from enum import IntEnum
from typing import Iterator, Optional

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

class IntcodeVM:
  # Program counter
  _pc: int

  # Relative base
  _relativeBase: int

  # Program data
  _memory: dict[int, int]

  # Input queue
  _inputQueue: deque[int]

  # Default value if input queue is empty
  _defaultInputValue: Optional[int]

  def __init__(self, memory: dict[int, int]) -> None:
    self._pc = 0
    self._relativeBase = 0
    self._memory = memory.copy()
    self._inputQueue = deque()
    self._defaultInputValue = None

  def addInput(self, value: int) -> None:
    self._inputQueue.append(value)

  def clearInputQueue(self) -> None:
    self._inputQueue = deque()

  def inputQueueSize(self) -> int:
    return len(self._inputQueue)

  def setDefaultInputValue(self, value: int) -> None:
    self._defaultInputValue = value

  # Runs the VM and returns a list of outputs. A "None" value within the
  # result means the machine is waiting for input.
  def run(self) -> Iterator[Optional[int]]:
    memory = self._memory

    while (value := memory[self._pc]) != 99:
      opcode = value % 100
      paramAddresses = self._getParameterAddresses()
      paramValues = [memory.get(x, 0) for x in paramAddresses]
      assert len(paramValues) == Op.getParamCount(opcode), \
        'bad paramValues for opcode: %d, %s' % (opcode, paramValues)

      # Asssume the destination is the last parameter, if it exists.
      dst = paramAddresses[-1]
      assert dst >= 0, 'dst cannot be negative'

      match opcode:
        case Op.ADD:
          memory[dst] = paramValues[0] + paramValues[1]
          self._pc += Op.getParamCount(opcode) + 1
        case Op.MUL:
          memory[dst] = paramValues[0] * paramValues[1]
          self._pc += Op.getParamCount(opcode) + 1
        case Op.INPUT:
          assert dst >= 0, 'dst cannot be negative'
          shouldYield = len(self._inputQueue) == 0
          if len(self._inputQueue) == 0:
            assert self._defaultInputValue is not None, \
              'input queue is empty and no default value set'
            memory[dst] = self._defaultInputValue
          else:
            memory[dst] = self._inputQueue.popleft()
          self._pc += Op.getParamCount(opcode) + 1
          if shouldYield:
            # None means the machine is waiting for input.
            yield None
        case Op.OUTPUT:
          self._pc += Op.getParamCount(opcode) + 1
          yield paramValues[0]
        case Op.JUMP_IF_TRUE:
          if paramValues[0] != 0:
            self._pc = paramValues[1]
          else:
            self._pc += Op.getParamCount(opcode) + 1
        case Op.JUMP_IF_FALSE:
          if paramValues[0] == 0:
            self._pc = paramValues[1]
          else:
            self._pc += Op.getParamCount(opcode) + 1
        case Op.LESS_THAN:
          memory[dst] = 1 if paramValues[0] < paramValues[1] else 0
          self._pc += Op.getParamCount(opcode) + 1
        case Op.EQUALS:
          memory[dst] = 1 if paramValues[0] == paramValues[1] else 0
          self._pc += Op.getParamCount(opcode) + 1
        case Op.RELATIVE_BASE:
          self._relativeBase += paramValues[0]
          self._pc += Op.getParamCount(opcode) + 1
        case _:
          assert False, 'bad opcode: %s' % opcode

  def _getParameterAddresses(self) -> list[int]:
    memory, pc = self._memory, self._pc
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
          address = memory.get(pc + i + 1, 0) + self._relativeBase
        case _:
          assert False, 'bad mode: %s' % mode
      # print('paramMode', pc, i, mode, address)
      results.append(address)
    assert len(results) <= 3, 'bad addresses: %s' % results
    # print('param', pc, self._relativeBase, value, opcode, paramModes, results)
    return results
