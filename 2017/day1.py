input = open('day1.txt').read()[:-1]

def ans(steps: int = 1) -> int:
  return sum([int(x) for i, x in enumerate(input) if input[i] == input[(i + steps) % len(input)]])

def part1() -> None:
  print(ans())

def part2() -> None:
  m = len(input)
  assert m % 2 == 0
  print(ans(m // 2))

part2()
