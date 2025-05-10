from common.md5 import md5hash

data = open('day4.txt').read().strip()

def find(n: int) -> int:
  i = 0
  while True:
    h = md5hash('%s%d' % (data, i))
    if h[:n] == '0' * n:
      return i
    i += 1

def part1() -> None:
  print(find(5))

def part2() -> None:
  print(find(6))

part2()
