from typing import Callable

input = open('day5.txt').read().splitlines()

def execute(instrs: list[int], handler: Callable[[int], int]) -> int:
  i = 0
  count = 0
  while 0 <= i < len(instrs):
    offset = instrs[i]
    instrs[i] += handler(offset)
    i += offset
    count += 1
  return count

def part1() -> None:
  instrs = list(map(int, input))
  print('instrs:', len(instrs))

  print(execute(instrs, lambda offset: 1))

def part2() -> None:
  instrs = list(map(int, input))
  print('instrs:', len(instrs))
  print(execute(instrs, lambda offset: -1 if offset >= 3 else 1))

part2()
