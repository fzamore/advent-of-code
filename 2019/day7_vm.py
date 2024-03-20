from itertools import cycle, permutations

from intcode import IntcodeVM

input = open('day7.txt').read().split(',')

def runSequence(memory: dict[int, int], seq: list[int]) -> int:
  assert len(seq) == 5, 'bad sequence'
  chainedValue = 0
  for seqValue in seq:
    for output in IntcodeVM(memory).addInputs([seqValue, chainedValue]).run():
      assert output is not None, 'not expecting extra input instruction'
      chainedValue = output
  return chainedValue

def runLoop(memory: dict[int, int], phases: list[int]) -> int:
  assert len(phases) == 5, 'bad phases'
  machines = [IntcodeVM(memory).addInput(p) for p in phases]

  chainedValue = 0
  for i in cycle(range(5)): # infinite cycle
    for output in machines[i].addInput(chainedValue).run():
      assert output is not None, 'not expecting input instruction'
      chainedValue = output
      break
    else:
      # If the machine halted, we won't hit the break statement and this
      # else block will execute. This means that the loop is finished.
      # This for-else seems a little sketchy, but it's exactly the
      # functionality I need.
      print('result for phases:', phases, chainedValue)
      return chainedValue

  assert False, 'should have hit halt opcode'

def part1() -> None:
  memory = dict(zip(range(len(input)), list(map(int, input))))
  print(max([runSequence(memory, list(s)) for s in permutations(range(5))]))

def part2() -> None:
  memory = dict(zip(range(len(input)), list(map(int, input))))
  print(max([runLoop(memory, list(s)) for s in permutations(range(5, 10))]))

part2()
