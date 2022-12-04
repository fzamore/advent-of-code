def getScore(char: str) -> int:
  assert(len(char) == 1)
  if char.islower():
    return ord(char) - 96
  else:
    return ord(char) - 38

def part1():
  total = 0
  for line in open('day3.txt').read().splitlines():
    c = len(line) // 2
    h1, h2 = line[:c], line[c:]
    assert(len(h1) == len(h2))
    v = set(h1) & set(h2)
    assert(len(v) == 1)
    total += getScore(v.pop())
  print(total)

def part2():
  total = 0
  num = 0
  for line in open('day3.txt').read().splitlines():
    if num % 3 == 0:
      s = set(line)

    s &= set(line)

    if num % 3 == 2:
      assert(len(s) == 1)
      total += getScore(s.pop())
    num += 1
  print(total)

part1()
