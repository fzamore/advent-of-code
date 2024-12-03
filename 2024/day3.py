from math import prod
import re
from common.ints import ints

input = open('day3.txt').read()

def part1() -> None:
  pattern = r'mul\(\d{1,3},\d{1,3}\)'
  matches = re.findall(pattern, input)
  print('matches:', len(matches))

  print(sum([prod(ints(m)) for m in matches]))

def part2() -> None:
  pattern = r'mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)'
  matches = re.findall(pattern, input)
  print('matches:', len(matches))

  enabled = True
  ans = 0
  for m in matches:
    v = m.split('(')
    match v[0]:
      case 'do':
        enabled = True
      case 'don\'t':
        enabled = False
      case 'mul':
        if enabled:
          ans += prod(ints(m))
      case _:
        assert False, 'bad token'
  print(ans)

part2()
