from common.ints import ints

data = open('day25.txt').read().rstrip()

def index(x: int, y: int) -> int:
  result = 1
  addend = 1
  for _ in range(y - 1):
    result += addend
    addend += 1

  addend = y + 1
  print('value at (0, y):', result)
  for _ in range(x - 1):
    result += addend
    addend += 1
  return result

def part1() -> None:
  y, x = ints(data)
  print('x, y:', x, y)

  exponent = index(x, y)
  start = 20151125
  base = 252533
  modulus = 33554393

  ans = start * pow(base, exponent - 1, modulus) % modulus
  print(ans)

part1()
