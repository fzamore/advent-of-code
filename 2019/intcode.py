from collections import deque
from enum import IntEnum
from typing import Iterable, Iterator, Optional

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
  _pc: int
  _relativeBase: int
  _memory: dict[int, int]
  _inputQueue: deque[int]

  def __init__(self, memory: dict[int, int]) -> None:
    self._pc = 0
    self._relativeBase = 0
    self._memory = memory.copy()
    self._inputQueue = deque()

  @staticmethod
  def initFromInput(input: list[str]) -> 'IntcodeVM':
    memory = dict(zip(range(len(input)), list(map(int, input))))
    return IntcodeVM(memory)

  def addInput(self, value: int) -> 'IntcodeVM':
    self._inputQueue.append(value)
    return self

  def addInputs(self, values: Iterable[int]) -> 'IntcodeVM':
    self._inputQueue.extend(values)
    return self

  def addAsciiInput(self, ascii: str) -> 'IntcodeVM':
    if ascii == '':
      return self
    for c in ascii:
      self.addInput(ord(c))
    self.addInput(ord('\n'))
    return self

  def clearInputQueue(self) -> 'IntcodeVM':
    self._inputQueue = deque()
    return self

  def inputQueueSize(self) -> int:
    return len(self._inputQueue)

  def copy(self) -> 'IntcodeVM':
    c = IntcodeVM(self._memory)
    c._pc = self._pc
    c._relativeBase = self._relativeBase
    c.addInputs(self._inputQueue)
    return c

  # Runs the VM and returns a list of outputs. Each individual output is
  # yielded, to allow callers to process outputs sequentially. A "None"
  # value within the result means the machine is waiting for input.
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

      # Whether we should advance the program counter.
      shouldAdvancePC = True

      match opcode:
        case Op.ADD:
          memory[dst] = paramValues[0] + paramValues[1]
        case Op.MUL:
          memory[dst] = paramValues[0] * paramValues[1]
        case Op.INPUT:
          assert dst >= 0, 'dst cannot be negative'
          if len(self._inputQueue) == 0:
            # Waiting for input.
            yield None
          memory[dst] = self._inputQueue.popleft()
        case Op.OUTPUT:
          # We advance the program counter before yielding back to
          # callers, to allow them to stop the machine and optionally
          # resume it later by calling run(). This ensures the program
          # counter is in the correct (advanced) spot at the beginning of
          # a subsequent run() call.
          self._pc += Op.getParamCount(opcode) + 1
          shouldAdvancePC = False
          yield paramValues[0]
        case Op.JUMP_IF_TRUE:
          if paramValues[0] != 0:
            self._pc = paramValues[1]
            shouldAdvancePC = False
        case Op.JUMP_IF_FALSE:
          if paramValues[0] == 0:
            self._pc = paramValues[1]
            shouldAdvancePC = False
        case Op.LESS_THAN:
          memory[dst] = 1 if paramValues[0] < paramValues[1] else 0
        case Op.EQUALS:
          memory[dst] = 1 if paramValues[0] == paramValues[1] else 0
        case Op.RELATIVE_BASE:
          self._relativeBase += paramValues[0]
        case _:
          assert False, 'bad opcode: %s' % opcode

      if shouldAdvancePC:
        # Advance program counter if necessary.
        self._pc += Op.getParamCount(opcode) + 1

  # Runs the machine and returns all outputs. This method will fail if
  # there are any input instructions and the input queue is empty.
  def runAll(self) -> list[int]:
    outputs = []
    for output in self.run():
      assert output is not None, 'runAll() cannot wait for input'
      outputs.append(output)
    return outputs

  # Runs the machine and halts when it encounters a single output
  # instruction. Returns the result of that output instruction.
  def runUntilSingleOutput(self) -> int:
    for output in self.run():
      assert output is not None, 'run() asked for input'
      return output
    assert False, 'run() did not produce an output'

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
      results.append(address)

    assert len(results) <= 3, 'bad addresses: %s' % results
    return results
