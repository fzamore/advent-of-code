input = open('day16.txt').read().strip()

def singleFFT(signal: str, patterns: list[tuple[int, int]]) -> str:
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
      section = signal[i:i + length]
      result += value * sum([int(x) for x in section])

    i += length
    pi = (pi + 1) % len(patterns)

  return str(abs(result) % 10)

def onePhase(signal: str, basePattern: list[int]) -> str:
  result = ''
  for i in range(len(signal)):
    patterns = [(i + 1, e) for e in basePattern]
    result += singleFFT(signal, patterns)
  return result

def part1() -> None:
  print('input length:', len(input))
  signal = input
  pattern = [0, 1, 0, -1]
  n = 100
  for _ in range(n):
    signal = onePhase(signal, pattern)

  print(''.join([str(s) for s in signal[:8]]))

part1()
