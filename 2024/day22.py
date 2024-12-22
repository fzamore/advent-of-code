input = open('day22.txt').read().splitlines()

def step(n: int) -> int:
  m = 16777216
  n = (n ^ (n * 64)) % m
  n = (n ^ (n // 32)) % m
  n = (n ^ (n * 2048)) % m
  return n

def part1() -> None:
  n = 2000
  ans = 0
  for line in input:
    secretNumber = int(line)
    for _ in range(n):
      secretNumber = step(secretNumber)
    ans += secretNumber
  print(ans)

part1()
