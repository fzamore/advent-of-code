from typing import AbstractSet, Optional
from common.ints import ints
from itertools import combinations
from math import prod

data = open('day8.txt').read().splitlines()
N = 1000

Coords = tuple[int, int, int]
Circuit = AbstractSet[Coords]

def parse() -> list[Coords]:
  r = []
  for line in data:
    v = tuple(ints(line))
    assert len(v) == 3, 'bad input'
    r.append(v)
  return r

def distSquared(c1: Coords, c2: Coords) -> int:
  return sum([(c1[i] - c2[i]) ** 2 for i in range(3)])

def solve(n: Optional[int] = None) -> tuple[list[Circuit], Coords, Coords]:
  coords = parse()
  pairs = []
  for c1, c2 in combinations(coords, 2):
    pairs.append((distSquared(c1, c2), c1, c2))
  pairs.sort()
  print('pairs:', len(pairs))
  circuits: set[Circuit] = set()
  for i, (_, c1, c2) in enumerate(pairs):
    if n is not None and i == n:
      # Part 1.
      return list(circuits), c1, c2

    # Find the circuit for each position.
    circuit1, circuit2 = None, None
    for c in circuits:
      if c1 in c:
        circuit1 = set(c)
      if c2 in c:
        circuit2 = set(c)

    circuit: Circuit = set()
    if circuit1 is None and circuit2 is None:
      circuit = set()
    elif circuit1 is None:
      assert circuit2 is not None, 'python typechecker is dumb'
      circuit = circuit2
      circuits.discard((circuit2))
    elif circuit2 is None:
      circuit = circuit1
      circuits.discard(circuit1)
    elif circuit1 != circuit2:
      # Merge
      circuits.discard(circuit1)
      circuits.discard(circuit2)
      circuit = circuit1.union(circuit2)
    else:
      # Already part of the same circuit; nothing to do.
      continue

    assert circuit is not None, 'should have set circuit'
    circuit.add(c1)
    circuit.add(c2)
    circuits.add(frozenset(circuit))

    if len(circuit) == len(data):
      # Part 2.
      return list(circuits), c1, c2

  assert False, 'should not reach here'

def part1() -> None:
  print('size:', len(data))
  circuits, _, _ = solve(N)
  sizes = sorted([len(x) for x in circuits], reverse=True)

  print('sizes:', len(circuits), sizes)
  print(prod(sizes[:3]))

def part2() -> None:
  print('size:', len(data))

  _, c1, c2 = solve()
  print('done:', c1, c2)
  print(c1[0] * c2[0])

part2()
