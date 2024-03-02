input = open('day16.txt').read().strip()

def singleFFT(signal: list[int], patterns: list[tuple[int, int]]) -> int:
  result = 0
  i = 0
  pi = 0
  first = True
  while i < len(signal):
    length, value = patterns[pi]
    assert length > 0, 'bad pattern length'
    assert value in [0, 1, -1], 'bad pattern value'

    if first:
      # Skip the first pattern value exactly once.
      length -= 1
      first = False

    if value != 0 and length != 0:
      result += value * sum(signal[i:i + length])

    i += length
    pi = (pi + 1) % len(patterns)

  return abs(result) % 10

def onePhase(signal: list[int], basePattern: list[int]) -> list[int]:
  result = []
  for i in range(len(signal)):
    patterns = [(i + 1, e) for e in basePattern]
    result.append(singleFFT(signal, patterns))
  return result

def part1() -> None:
  print('input length:', len(input))
  signal = list(map(int, input))
  pattern = [0, 1, 0, -1]
  n = 100
  for _ in range(n):
    signal = onePhase(signal, pattern)

  print(''.join([str(s) for s in signal[:8]]))

part1()
