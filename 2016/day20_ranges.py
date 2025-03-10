from common.ints import ints
from common.ranges import subtractMultipleRanges

input = open('day20.txt').read().splitlines()

def parseInput() -> list[range]:
  r = []
  for line in input:
    a, b = ints(line)
    assert b < 0, 'ints() should parse a dash as negative'
    r.append(range(a, -b))
  return r

def part2() -> None:
  ranges = parseInput()
  print('ranges:', len(ranges))

  hi = 4294967295
  freelist = subtractMultipleRanges(range(0, hi), ranges)
  print('freelist size:', len(freelist))

  # For some reason, each entry in the freelist contains only a single IP.
  # As far as I can tell, this isn't a requirement of the problem.
  for r in freelist:
    assert r.stop - r.start == 0, 'expecting freelist to contain only singletons'

  s = sum([r.stop - r.start + 1 for r in freelist])
  print(s)

part2()
