from common.ints import ints

input = open('day3.txt').read().splitlines()

def isValidTriangle(a: int, b: int, c: int) -> bool:
  return a + b > c and a + c > b and b + c > a

def part1() -> None:
  valid = 0
  for line in input:
    a, b, c = ints(line)
    if isValidTriangle(a, b, c):
      valid += 1
  print(valid)

def part2() -> None:
  assert len(input) % 3 == 0, 'bad input'
  valid = 0
  i = 0
  while i < len(input):
    t1, t2, t3 = [], [], []
    for j in range(3):
      a, b, c = ints(input[i + j])
      t1.append(a)
      t2.append(b)
      t3.append(c)
    assert len(t1) == len(t2) == len(t3) == 3, 'bad triplets'

    for a, b, c in [t1, t2, t3]:
      if isValidTriangle(a, b, c):
        valid += 1

    i += 3

  print(valid)

part2()
