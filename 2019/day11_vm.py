from common.sparsegrid import SparseGrid
from intcode import IntcodeVM

input = open('day11.txt').read().split(',')

def updateHeading(heading: tuple[int, int], *, leftTurn: bool) -> tuple[int, int]:
  match heading:
    case (0, -1): # up
      return (-1, 0) if leftTurn else (1, 0)
    case (-1, 0): # left
      return (0, 1) if leftTurn else (0, -1)
    case (0, 1): # down
      return (1, 0) if leftTurn else (-1, 0)
    case (1, 0): # right
      return (0, -1) if leftTurn else (0, 1)
    case _:
      assert False, 'invalid heading: %s' % str(heading)

def runMachine(machine: IntcodeVM, grid: SparseGrid) -> None:
  px, py = (0, 0)
  heading = (0, -1)
  outputCount = 0
  for output in machine.run():
    if output is None:
      machine.addInput(grid.getValue((px, py), 0))
      continue

    if outputCount % 2 == 0:
      grid.setValue((px, py), output)
    else:
      heading = updateHeading(heading, leftTurn=(output == 0))
      px, py = px + heading[0], py + heading[1]
    outputCount += 1

def part1() -> None:
  machine = IntcodeVM.initFromInput(input).addInput(0)
  grid = SparseGrid(2)
  runMachine(machine, grid)
  print(len(grid.getAllCoords()))

def part2() -> None:
  machine = IntcodeVM.initFromInput(input).addInput(1)
  grid = SparseGrid(2)
  runMachine(machine, grid)
  grid.print2D(default=' ', charMap = {1: '#', 0: ' '})

part2()
