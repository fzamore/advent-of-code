from common.ints import ints

input = open('day20.txt').read().splitlines()

def parseInput() -> list[tuple[int, int]]:
  r = []
  for line in input:
    a, b = ints(line)
    assert b < 0
    r.append((a, -b))
  return r

def findFreeIPs(ranges: list[tuple[int, int]]) -> list[int]:
  hi = 4294967295

  guesses = []
  guess = 0
  while guess <= hi:
    for a, b in ranges:
      if a <= guess <= b:
        # This guess is in a blacklisted range. The next guess should be
        # the lowest integer greater than this range.
        guess = b + 1
        break
    else:
      # This guess isn't blacklisted.
      guesses.append(guess)
      guess += 1
  return guesses

def part1() -> None:
  ranges = parseInput()
  print('ranges:', len(ranges))

  guesses = findFreeIPs(ranges)
  print(min(guesses))

def part2() -> None:
  ranges = parseInput()
  print('ranges:', len(ranges))

  guesses = findFreeIPs(ranges)
  print(len(guesses))

part2()
