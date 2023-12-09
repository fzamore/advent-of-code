input = open('day9.txt').read().splitlines()

def computeNewValuesForSequence(seq: list[int]) -> tuple[int, int]:
  assert len(seq) > 1, 'bad sequence'
  first, last = seq[0], seq[-1]
  mul = -1
  s = seq
  while len(set(s)) > 1:
    s = [s[i + 1] - s[i] for i in range(len(s) - 1)]
    # To compute the new first element, alternate between adding and
    # subtracting the first element of each iteration.
    first += mul * s[0]
    mul *= -1

    # To compute the new last element, add the last element of each iteration.
    last += s[-1]
  return first, last

def part1():
  seqs = [list(map(int, x.split())) for x in input]
  print('sequence count:', len(seqs))

  s = sum([computeNewValuesForSequence(x)[1] for x in seqs])
  print(s)

def part2():
  seqs = [list(map(int, x.split())) for x in input]
  print('sequence count:', len(seqs))

  s = sum([computeNewValuesForSequence(x)[0] for x in seqs])
  print(s)

part2()
