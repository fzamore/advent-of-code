from collections import namedtuple
from dataclasses import dataclass
from enum import IntEnum
from itertools import cycle
from typing import Optional

input = open('day23.txt').read().split(',')

Packet = namedtuple('Packet', ['address', 'x', 'y'])

@dataclass
class Machine:
  memory: dict[int, int]
  queue: list[int]
  pc: int

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

def runMachine(memory: dict[int, int], inputs: list[int], pc: int) \
  -> tuple[int, Optional[Packet]]:
  outgoingPacket = []

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
        stop = len(inputs) == 0
        memory[dst] = inputs.pop(0) if len(inputs) > 0 else -1
        pc += Op.getParamCount(opcode) + 1
        if stop:
          return pc, None
      case Op.OUTPUT:
        o = paramValues[0]
        outgoingPacket.append(o)
        pc += Op.getParamCount(opcode) + 1
        if len(outgoingPacket) == 3:
          return pc, Packet(outgoingPacket[0], outgoingPacket[1], outgoingPacket[2])
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

  return pc, None

def initMachines(n: int) -> dict[int, Machine]:
  memory = dict(zip(range(len(input)), list(map(int, input))))
  machines: dict[int, Machine] = {}
  for i in range(n):
    machines[i] = Machine(memory.copy(), [i], 0)
  return machines

def part1() -> None:
  n = 50
  machines = initMachines(n)
  for i in cycle(range(n)):
    machine = machines[i]
    print('running machine:', i)
    pc, result = runMachine(machine.memory, machine.queue, machine.pc)
    machines[i].pc = pc

    if result is None:
      continue

    print('received packet:', result)
    paddress, x, y = result
    if paddress == 255:
      print('done:', result)
      print(y)
      return

    assert paddress < n, 'bad packet address'
    machines[paddress].queue.append(x)
    machines[paddress].queue.append(y)

def part2() -> None:
  n = 50
  machines = initMachines(n)

  natX, natY, lastZeroY = None, None, None
  idleSet: set[int] = set()
  for i in cycle(range(n)):
    # We need to complete two empty revolutions per machine to conclude
    # that we're idle.
    isIdle = all([len(machines[m].queue) == 0 for m in range(n)]) \
      and len(idleSet) == 2 * n
    if isIdle:
      print('idle:', lastZeroY)
      if natY == lastZeroY:
        print('done')
        print(lastZeroY)
        return

      assert natX is not None and natY is not None, 'missing nat packet when idle'
      # Reset the zero queue to only the most recent nat packet.
      machines[0].queue = [natX, natY]
      lastZeroY = natY

      # Reset the nat packet and idle set.
      natX, natY = None, None
      idleSet = set()
      continue

    machine = machines[i]
    pc, result = runMachine(machine.memory, machine.queue, machine.pc)
    machine.pc = pc

    if result is None:
      # Add at most two entries for each machine into the idle set.
      idleSet.add(i if i not in idleSet else i + n)
      continue

    paddress, x, y = result
    if paddress == 255:
      print('nat packet:', result)
      natX, natY = x, y
      continue

    assert paddress < n, 'bad packet address'
    machines[paddress].queue.append(x)
    machines[paddress].queue.append(y)

part2()
