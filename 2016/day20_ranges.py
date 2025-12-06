from common.ints import ints
from common.ranges import Range, subtractMultipleRanges

input = open('day20.txt').read().splitlines()

def parseInput() -> list[Range]:
  r = []
  for line in input:
    a, b = ints(line)
    assert b < 0, 'ints() should parse a dash as negative'
    r.append((a, -b))
  return r

def part2() -> None:
  ranges = parseInput()
  print('ranges:', len(ranges))

  hi = 4294967295
  freelist = subtractMultipleRanges((0, hi), ranges)
  print('freelist size:', len(freelist))

  # For some reason, each entry in the freelist contains only a single IP.
  # As far as I can tell, this isn't a requirement of the problem.
  for start, end in freelist:
    assert end - start == 0, 'expecting freelist to contain only singletons'

  s = sum([end - start + 1 for (start, end) in freelist])
  print(s)

part2()
