from collections import Counter

input = open('day1.txt').read().splitlines()

def parseInput() -> tuple[list[int], list[int]]:
  l1, l2 = [], []
  for line in input:
    n1, n2 = map(int, line.split())
    l1.append(n1)
    l2.append(n2)
  assert len(l1) == len(l2), 'lists are not the same length'
  return l1, l2

def part1() -> None:
  l1, l2 = parseInput()

  l1 = sorted(l1)
  l2 = sorted(l2)
  ans = sum([abs(l1[i] - l2[i]) for i in range(len(l1))])
  print(ans)

def part2() -> None:
  l1, l2 = parseInput()

  d = Counter(l2)
  ans = sum([n * d[n] for n in l1])
  print(ans)

part2()
