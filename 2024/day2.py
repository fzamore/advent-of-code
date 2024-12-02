from common.ints import ints

input = open('day2.txt').read().splitlines()

Level = list[int]

def isSafe(level: Level) -> bool:
  assert len(level) >= 2, 'level too short'

  isIncreasing = level[1] > level[0]
  for i in range(len(level) - 1):
    d = level[i+1] - level[i]
    if d == 0 or abs(d) > 3:
      return False
    if d > 0 and not isIncreasing:
      return False
    if d < 0 and isIncreasing:
      return False
  return True

def part1() -> None:
  print('levels:', len(input))
  print(sum([1 for line in input if isSafe(ints(line))]))

def part2() -> None:
  print('levels:', len(input))
  safeLevels = 0
  for line in input:
    level = ints(line)
    if isSafe(level):
      safeLevels += 1
      continue

    for i in range(len(level)):
      levelCopy = level.copy()
      levelCopy.pop(i)
      assert len(levelCopy) + 1 == len(level), 'did not remove from copy'
      if isSafe(levelCopy):
        safeLevels += 1
        break
  print(safeLevels)

part2()
