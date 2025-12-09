from common.ints import ints
from itertools import combinations

data = open('day9.txt').read().splitlines()

def part1() -> None:
  coords = [ints(line) for line in data]
  print('coords:', len(coords))

  mx = -1
  for c1, c2 in combinations(coords, 2):
    (x1, y1), (x2, y2) = c1, c2
    area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
    mx = max(mx, area)
  print(mx)

part1()
