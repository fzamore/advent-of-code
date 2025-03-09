from common.ints import ints

input = open('day15.txt').read().splitlines()

Disc = tuple[int, int, int]

def parseInput() -> list[Disc]:
  discs = []
  for line in input:
    k, m, t, p = ints(line)
    assert t == 0, 'time should be zero in input'
    discs.append((p, k, m))
  return discs

def solveSingle(disc: Disc) -> tuple[int, int]:
  p, k, m = disc
  t = (-p - k) % m
  return t, m

def solve(discs: list[Disc]) -> int:
  n = 10_000_000 # Chosen by experimentation

  # Solve for t (mod each disc), and then compute intersection of all ranges.
  s = None
  for disc in discs:
    t, m = solveSingle(disc)

    rng = set(range(t, n, m))
    if s is None:
      s = rng
    else:
      s.intersection_update(rng)

  assert s is not None, 'should have initialized set'
  print('ix count:', len(s))
  return min(s)

def part1() -> None:
  discs = parseInput()
  print('discs:', len(discs))

  print(solve(discs))

def part2() -> None:
  discs = parseInput()
  discs.append((0, len(discs) + 1, 11))
  print('discs:', len(discs))

  print(solve(discs))

part2()
