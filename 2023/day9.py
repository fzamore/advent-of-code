input = open('day9.txt').read().splitlines()

def computeValueForSequence(seq: list[int]) -> int:
  assert len(seq) > 1, 'bad sequence'
  result = seq[-1]
  s = seq
  while len(set(s)) > 1:
    s = [s[i + 1] - s[i] for i in range(len(s) - 1)]
    result += s[-1]
  return result

def part1():
  seqs = [list(map(int, x.split())) for x in input]
  print(len(seqs))

  s = sum([computeValueForSequence(x) for x in seqs])
  print(s)

part1()
