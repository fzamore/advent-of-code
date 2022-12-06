def findMarkerStart(input: str, count: int) -> int:
  for i in range(count, len(input)):
    if len(set(input[i-count:i])) == count:
      return i
  assert False, 'did not find marker'

def part1():
  input = open('day6.txt').read()
  print(findMarkerStart(open('day6.txt').read(), 4))

def part2():
  input = open('day6.txt').read()
  print(findMarkerStart(open('day6.txt').read(), 14))

part2()
