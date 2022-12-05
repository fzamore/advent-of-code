from collections import defaultdict
from typing import cast

def parseInput(filename: str) -> tuple[
  int, # bucket count
  defaultdict[int, list[str]], # map of bucket to items
  list[tuple[int, int, int]], # list of instructions(qty, src, dst)
]:
  input = open(filename).read()
  bucketsStr, instructionsStr = [s.splitlines() for s in input.split("\n\n")]
  count = max(map(int, bucketsStr[-1].split()))

  buckets: defaultdict[int, list[str]] = defaultdict(list)
  for line in bucketsStr[:-1]:
    for b in range(1, count + 1):
      strI = 4 * (b - 1) + 1
      if strI < len(line):
        v = line[strI]
        if v != ' ':
          # insert at the bottom, since we encounter them from top to bottom
          buckets[b].insert(0, v)

  # get every other item in the instructions string
  instructions = [cast(
    tuple[int, int, int],
    tuple(map(int, v.split()[1::2])),
  ) for v in instructionsStr]
  return (count, buckets, instructions)

def part1():
  count, buckets, instructions = parseInput('day5.txt')

  print('bucket count: %d' % count)

  print(buckets)

  for qty, src, dst in instructions:
    for i in range(qty):
      buckets[dst].append(buckets[src].pop())

  print(buckets)
  print(''.join([buckets[s][-1] for s in range(1, count + 1)]))

def part2():
  count, buckets, instructions = parseInput('day5.txt')

  print('bucket count: %d' % count)

  for qty, src, dst in instructions:
    print(qty, src, dst)
    buckets[dst].extend(buckets[src][-qty:])
    buckets[src] = buckets[src][:-qty]
    print(buckets)

  print(buckets)
  print(''.join([buckets[s][-1] for s in range(1, count + 1)]))

part2()
