from enum import IntEnum
from intcode import IntcodeVM

input = open('day13.txt').read().split(',')

class Type(IntEnum):
  EMPTY = 0
  WALL = 1
  BLOCK = 2
  PADDLE = 3
  BALL = 4

def part1() -> None:
  machine = IntcodeVM.initFromInput(input)
  count = 0
  for i, output in enumerate(machine.run()):
    assert output is not None, 'unexpected input'
    if i % 3 == 2 and output == Type.BLOCK:
      # This is the third element of the triplet and it's of type block.
      count += 1
  print(count)

def part2() -> None:
  print()
  print('start:')

  memory = dict(zip(range(len(input)), list(map(int, input))))
  memory[0] = 2
  machine = IntcodeVM(memory)

  outputs = []
  paddle = None
  ballX = None
  lastScore = None
  for output in machine.run():
    if output is None:
      # The only thing we need to do is keep the paddle under the ball. We
      # don't need to keep track of bricks.
      assert ballX is not None, 'ballX not set'
      if ballX < paddle:
        joy = -1
      elif ballX > paddle:
        joy = 1
      else:
        joy = 0
      machine.addInput(joy)
      continue

    outputs.append(output)
    if len(outputs) == 3:
      x, y, type = outputs
      outputs = []

      if x == -1 and y == 0:
        print('score:', type)
        lastScore = type
        continue

      match type:
        case Type.EMPTY: pass
        case Type.WALL: pass
        case Type.BLOCK: pass
        case Type.PADDLE: paddle = x
        case Type.BALL: ballX = x
        case _: assert False, 'bad outputs'

  print(lastScore)

part2()
