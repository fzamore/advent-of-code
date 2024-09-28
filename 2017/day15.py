input = open('day15.txt').read().splitlines()

def parseInput() -> tuple[int, int]:
  assert len(input) == 2, 'bad input'
  return int(input[0].split()[-1]), int(input[1].split()[-1])

def genA(a: int, multiple: int = 1) -> int:
  m = 2147483647
  fa = 16807
  while (na := (a * fa) % m) % multiple != 0:
    a = na
  return na

def genB(b: int, multiple: int = 1) -> int:
  m = 2147483647
  fb = 48271
  while (nb := (b * fb) % m) % multiple != 0:
    b = nb
  return nb

def part1() -> None:
  a, b = parseInput()

  print('input:', a, b)

  # This is very slow.
  n = 40000000
  c = 0
  for _ in range(n):
    if (a & 0xffff) == (b & 0xffff):
      c += 1
    a, b = genA(a), genB(b)
  print(c)

def part2() -> None:
  a, b = parseInput()

  print('input:', a, b)

  n = 5000000
  c = 0
  for _ in range(n):
    if (a & 0xffff) == (b & 0xffff):
      c += 1
    a, b = genA(a, 4), genB(b, 8)
  print(c)

part2()
