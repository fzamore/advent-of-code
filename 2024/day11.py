from collections import Counter
from common.ints import ints

input = open('day11.txt').read().rstrip()

def blinkSingleStone(stone: int) -> list[int]:
  if stone == 0:
    return [1]

  stoneString = str(stone)
  n = len(stoneString)
  if n % 2 == 0:
    return [int(stoneString[:(n // 2)]), int(stoneString[(n // 2):])]

  return [stone * 2024]

# Naive approach of blinking each stone sequentially.
def blinkSlow(stones: list[int]) -> list[int]:
  result = []
  for s in stones:
    result.extend(blinkSingleStone(s))
  return result

# This approach keeps a count of each distinct stone, so we only have to
# blink each unique stone once per round. This approach takes advantage of
# two things: a/ the order of the stones doesn't matter, and b/ there are
# relatively few distinct stones.
def blinkFast(stoneCounts: dict[int, int]) -> dict[int, int]:
  result: dict = Counter()
  for stone in stoneCounts:
    for newStone in blinkSingleStone(stone):
      result[newStone] += stoneCounts[stone]
  return result

def part1() -> None:
  stones = ints(input)
  print('stones:', stones)
  n = 25
  for _ in range(n):
    stones = blinkSlow(stones)

  print(len(stones))

def part2() -> None:
  stones = tuple(ints(input))
  print('stones:', stones)

  n = 75
  stoneCounts: dict = Counter(stones)
  for _ in range(n):
    stoneCounts = blinkFast(stoneCounts)
  print('distinct stones:', len(stoneCounts))
  print(sum(stoneCounts.values()))

part2()
