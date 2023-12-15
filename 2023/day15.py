input = open('day15.txt').read().splitlines()[0].split(',')

def algo(s: str) -> int:
  acc = 0
  for c in s:
    acc += ord(c)
    acc *= 17
    acc %= 256
  return acc

def part1():
  print(sum([algo(s) for s in input]))

part1()
