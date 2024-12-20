from functools import cache

input = open('day19.txt').read().splitlines()

def parseInput() -> tuple[list[str], list[str]]:
  towels = None
  patterns: list[str] = []
  for line in input:
    if line == '':
      continue
    if towels is None:
      towels = line.split(', ')
    else:
      patterns.append(line)

  assert towels is not None, 'did not find towels'
  return towels, patterns

@cache
def countMatches(towels: tuple[str], pattern: str) -> int:
  if pattern == '':
    return 1

  # Add up all recursive calls of the pattern substring after stripping
  # off the towel prefix.
  return sum([countMatches(towels, pattern[len(t):]) for t in towels if pattern.startswith(t)])

def part1() -> None:
  towels, patterns = parseInput()
  print('data:', len(towels), len(patterns))

  ans = sum([1 for p in patterns if countMatches(tuple(towels), p) > 0])
  print(ans)

def part2() -> None:
  towels, patterns = parseInput()
  print('data:', len(towels), len(patterns))

  ans = sum([countMatches(tuple(towels), p) for p in patterns])
  print(ans)

part2()
