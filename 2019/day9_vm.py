from intcode import IntcodeVM

input = open('day9.txt').read().split(',')

def part1() -> None:
  print(IntcodeVM.initFromInput(input).addInput(1).runAll()[0])

def part2() -> None:
  print(IntcodeVM.initFromInput(input).addInput(2).runAll()[0])

part2()
