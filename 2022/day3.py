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
    v = set(h1).intersection(set(h2))
    assert(len(v) == 1)
    char = v.pop()
    s = getScore(char)
    print(s)
    total += s
  print(total)

def part2():
  total = 0
  num = 0
  for line in open('day3.txt').read().splitlines():
    if num % 3 == 0:
      sets = {}

    sets[num % 3] = set(line)

    if num % 3 == 2:
      v = set.intersection(*sets.values())
      assert(len(v) == 1)
      char = v.pop()
      print(char)
      s = getScore(char)
      total += s
    num += 1
  print(total)

part2()
