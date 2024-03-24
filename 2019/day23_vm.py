from itertools import cycle
from typing import Optional

from intcode import IntcodeVM

input = open('day23.txt').read().split(',')

def initMachines(n: int) -> dict[int, IntcodeVM]:
  machines: dict[int, IntcodeVM] = {}
  for i in range(n):
    machines[i] = IntcodeVM.initFromInput(input).addInput(i)
  return machines

def runMachine(machine: IntcodeVM) -> Optional[tuple[int, int, int]]:
  packet = []
  if machine.inputQueueSize() == 0:
    # Use -1 if the queue is empty.
    machine.addInput(-1)

  for output in machine.run():
    if output is None:
      # Do not synthesize a packet if we're waiting for input.
      return None

    packet.append(output)
    if len(packet) == 3:
      return (packet[0], packet[1], packet[2])

  assert False, 'machine did not run cleanly'

def part1() -> None:
  n = 50
  machines = initMachines(n)
  for i in cycle(range(n)):
    packet = runMachine(machines[i])
    if packet is None:
      continue

    print('received packet from i:', i, packet)
    paddress, x, y = packet
    if paddress == 255:
      print('done:', packet)
      print(y)
      return

    assert paddress < n, 'bad packet address: %d' % paddress
    machines[paddress].addInputs([x, y])

def part2() -> None:
  n = 50
  machines = initMachines(n)

  natX, natY, lastZeroY = None, None, None
  idleSet: set[int] = set()
  for i in cycle(range(n)):
    # We need to complete two empty revolutions per machine to conclude
    # that we're idle.
    isIdle = all([machines[m].inputQueueSize() == 0 for m in range(n)]) \
      and len(idleSet) == 2 * n
    if isIdle:
      print('idle:', lastZeroY)
      if natY == lastZeroY:
        print('done')
        print(lastZeroY)
        return

      assert natX is not None and natY is not None, 'missing nat packet when idle'
      # Reset the zero queue to only the most recent nat packet.
      machines[0].clearInputQueue().addInputs([natX, natY])
      lastZeroY = natY

      # Reset the nat packet and idle set.
      natX, natY = None, None
      idleSet = set()
      continue

    packet = runMachine(machines[i])
    if packet is None:
      # We're waiting for input. Add at most two entries for each machine
      # into the idle set.
      idleSet.add(i if i not in idleSet else i + n)
      continue

    paddress, x, y = packet
    if paddress == 255:
      print('nat packet:', packet)
      natX, natY = x, y
      continue

    assert paddress < n, 'bad packet address: %d' % paddress
    machines[paddress].addInputs([x, y])

part2()
