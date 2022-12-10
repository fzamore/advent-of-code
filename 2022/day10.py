input = open('day10.txt').read().splitlines()

def getCyclesPerInstr(instr: str) -> int:
  return {
    'noop': 1,
    'addx': 2,
  }[instr]

def getValueAtCycle(cycles: list[int], cycle: int) -> int:
  return cycles[cycle - 1]

def getSignalStrengthAtCycle(cycles: list[int], cycle: int) -> int:
  return getValueAtCycle(cycles, cycle) * cycle

def part1():
  x = 1
  cycles = []
  for line in input:
    tokens = line.split()
    instr = tokens[0]
    [cycles.append(x) for _ in range(getCyclesPerInstr(instr))]
    if instr == 'addx':
      x += int(tokens[1])

  print(sum([getSignalStrengthAtCycle(cycles, i)
    for i in [20, 60, 100, 140, 180, 220]]))


part1()
