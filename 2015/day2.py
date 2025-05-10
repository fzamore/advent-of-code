from common.ints import ints

data = open('day2.txt').read().splitlines()

def surfaceArea(line: str) -> int:
  a, b, c = ints(line)
  x, y, z = a * b, b * c, c * a
  return 2 * (x + y + z) + min(x, y, z)

def perim(a: int, b: int) -> int:
  return 2 * (a + b)

def ribbon(line: str) -> int:
  a, b, c = ints(line)
  return min(perim(a, b), perim(b, c), perim(c, a)) + a * b * c

def part1() -> None:
  print(sum([surfaceArea(l) for l in data]))

def part2() -> None:
  print(sum([ribbon(l) for l in data]))

part2()
