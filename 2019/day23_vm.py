from itertools import cycle

from intcode import IntcodeVM

input = open('day23.txt').read().split(',')

def initMachines(n: int) -> dict[int, IntcodeVM]:
  memory = dict(zip(range(len(input)), list(map(int, input))))
  machines: dict[int, IntcodeVM] = {}
  for i in range(n):
    machines[i] = IntcodeVM(memory)
    machines[i].addInput(i)
    machines[i].setDefaultInputValue(-1)
  return machines

def part1() -> None:
  n = 50
  machines = initMachines(n)
  for i in cycle(range(n)):
    packet = []
    for output in machines[i].run():
      if output is None:
        # Skip input instructions.
        break

      packet.append(output)
      if len(packet) == 3:
        print('received packet from i:', i, packet)
        paddress, x, y = packet
        if paddress == 255:
          print('done:', packet)
          print(y)
          return

        assert paddress < n, 'bad packet address'
        machines[paddress].addInput(x)
        machines[paddress].addInput(y)
        break

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
      machines[0].clearInputQueue()
      machines[0].addInput(natX)
      machines[0].addInput(natY)
      lastZeroY = natY

      # Reset the nat packet and idle set.
      natX, natY = None, None
      idleSet = set()
      continue

    packet = []
    for output in machines[i].run():
      if output is None:
        # We're waiting for input. Add at most two entries for each machine
        # into the idle set.
        idleSet.add(i if i not in idleSet else i + n)
        break

      packet.append(output)
      if len(packet) == 3:
        paddress, x, y = packet
        if paddress == 255:
          print('nat packet:', packet)
          natX, natY = x, y
          break

        assert paddress < n, 'bad packet address'
        machines[paddress].addInput(x)
        machines[paddress].addInput(y)
        break

part2()
