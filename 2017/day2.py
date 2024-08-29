from itertools import combinations

input = open('day2.txt').read().splitlines()

def part1() -> None:
  ans = 0
  for line in input:
    v = list(map(int, line.split()))
    ans += max(v) - min(v)
  print(ans)

def part2() -> None:
  ans = 0
  for line in input:
    v = list(map(int, line.split()))
    for a, b in combinations(v, 2):
      if a == 0 or b == 0:
        continue
      if a % b == 0:
        ans += a // b
      elif b % a == 0:
        ans += b // a

  print(ans)

part2()
