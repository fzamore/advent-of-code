from math import ceil, sqrt

def parse(filename: str) -> list[int]:
  return list(map(int, open(filename).read().split(',')))

def part1() -> None:
  data = parse('quest1.1.txt')
  print('data:', len(data))

  def f(x: int) -> int:
    return ceil(sqrt(x)) ** 2 - x

  print(sum(map(f, data)))

def part2() -> None:
  data = parse('quest1.2.txt')
  def f(x: int) -> int:
    return 8 - x if x <= 8 else (4 - (x % 4)) % 4

  print(sum(map(f, data)))

def part3() -> None:
  data = parse('quest1.3.txt')
  def f(x: int) -> int:
    n = ceil(sqrt(x))
    if n % 2 == 0:
      n += 1
    elif (n ** 2) - 1 < x:
      n += 2
    return (n ** 2) - 1 - x

  print(sum(map(f, data)))

part3()
