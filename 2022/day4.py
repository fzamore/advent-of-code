def completelyContains(outer: tuple, inner: tuple):
  return outer[0] <= inner[0] and outer[1] >= inner[1]

def overlaps(e1: tuple, e2: tuple):
  return e2[0] <= e1[1] and e1[0] <= e2[1]

def part1():
  count = 0
  for line in open('day4.txt').read().splitlines():
    # each elf is a (x,y) range tuple
    e1, e2 = [tuple(map(int, s.split('-'))) for s in line.split(',')]
    if completelyContains(e1, e2) or completelyContains(e2, e1):
      count += 1
  print(count)

def part2():
  count = 0
  for line in open('day4.txt').read().splitlines():
    # each elf is a (x,y) range tuple
    e1, e2 = [tuple(map(int, s.split('-'))) for s in line.split(',')]
    if overlaps(e1, e2):
      count += 1
  print(count)

part2()
