from collections import namedtuple
from itertools import combinations
from typing import Iterator, Optional

input = open('day3.txt').read().splitlines()

Coords = tuple[int, int]
Claim = namedtuple('Claim', ['id', 'x', 'y', 'w', 'h'])

def parseLine(line: str) -> Claim:
  # #1 @ 1,3: 4x4
  v = line.split(' @ ')[1].split(': ')
  assert len(v) == 2, 'bad line'
  id = int(line.split(' @ ')[0][1:])
  x = int(v[0].split(',')[0])
  y = int(v[0].split(',')[1])
  w = int(v[1].split('x')[0])
  h = int(v[1].split('x')[1])
  return Claim(id, x, y, w, h)

def get1DIntersection(a1: int, a2: int, b1: int, b2: int) -> Optional[Coords]:
  if b1 > a2 or a1 > b2:
    return None
  return max(a1, b1), min(a2, b2)

# Finds the interssection of the two claims by finding the two 1D
# intersections in each dimension and then returning each point in the
# resulting rectangle.
def getIntersection(c1: Claim, c2: Claim) -> Iterator[Coords]:
  ixx = get1DIntersection(c1.x, c1.x + c1.w - 1, c2.x, c2.x + c2.w - 1)
  ixy = get1DIntersection(c1.y,	c1.y + c1.h - 1, c2.y, c2.y + c2.h - 1)
  if ixx is None or ixy is None:
    return []

  for y in range(ixy[0], ixy[1] + 1):
    for x in range(ixx[0], ixx[1] + 1):
      yield x, y

# Finds the intersection of the two claims by iterating over every single
# point in C1 and checks whether it's in C2. This is slow (30s on phone,
# 43s on laptop).
def getIntersectionSlow(c1: Claim, c2: Claim) -> Iterator[Coords]:
  for y in range(c1.y, c1.y + c1.h):
    for x in range(c1.x, c1.x + c1.w):
      if c2.x <= x < c2.x + c2.w and c2.y <= y < c2.y + c2.h:
        yield x, y

def hasIntersection(c1: Claim, c2: Claim) -> bool:
  for _ in getIntersection(c1, c2):
    return True
  return False

def part1() -> None:
  claims = [parseLine(line) for line in input]
  print('claims:', len(claims))

  ix: set[Coords] = set()
  for c1, c2 in combinations(claims, 2):
    ix.update(getIntersection(c1, c2))

  print(len(ix))

def part2() -> None:
  claims = [parseLine(line) for line in input]
  print('claims:', len(claims))

  working = set([c.id for c in claims])
  for c1, c2 in combinations(claims, 2):
    if c1.id not in working and c2.id not in working:
      continue

    if hasIntersection(c1, c2):
      working.discard(c1.id)
      working.discard(c2.id)

  print(working)
  assert len(working) == 1, 'found more than 1 ans'
  [print(x) for x in working]

part2()
