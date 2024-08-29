from collections import Counter

input = open('day4.txt').read().splitlines()

def part1() -> None:
  ans = 0
  for line in input:
    c = Counter(line.split())
    if c.most_common(1)[0][1] == 1:
      ans += 1
  print(ans)

def part2() -> None:
  ans = 0
  for line in input:
    c = Counter([''.join(sorted(x)) for x in line.split()])
    if c.most_common(1)[0][1] == 1:
      ans += 1
  print(ans)

part2()
