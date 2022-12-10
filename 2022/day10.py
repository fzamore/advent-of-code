GRID_WIDTH = 40

input = open('day10.txt').read().splitlines()

def getCyclesPerInstr(instr: str) -> int:
  return {
    'noop': 1,
    'addx': 2,
  }[instr]

def getSignalStrengthAtCycle(cycles: list[int], cycle: int) -> int:
  valueAtCycle = cycles[cycle - 1]
  return valueAtCycle * cycle

def printPixel(px: int, x: int) -> None:
  if x - 1 <= px <= x + 1:
    print('#', end='')
  else:
    print('.', end='')

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

def part2():
  px = 0
  x = 1
  for line in input:
    tokens = line.split()
    instr = tokens[0]
    for _ in range(getCyclesPerInstr(instr)):
      printPixel(px, x)
      px += 1
      if px == GRID_WIDTH:
        # end of line. print a newline
        print()
        px = 0
    if instr == 'addx':
      x += int(tokens[1])

part2()
