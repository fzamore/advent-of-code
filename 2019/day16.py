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

# Computes the n-phase FFT from the end, assumming that the pattern is
# composed entirely of 1's. We can make this assumption only if we're
# computing at most half of the signal starting from the end. The pattern
# will not be entirely 1's if we consider more than that.
def computeFFTFromEnd(signal: list[int], n: int, qty: int) -> list[int]:
  assert qty <= len(signal) // 2, 'cannot process more than last half of signal'
  subsignal = signal[-qty:]
  for _ in range(n):
    # Compute a running sum from the back.
    value = 0
    for i in range(1, len(subsignal) + 1):
      value += subsignal[-i]
      # Process in-place.
      subsignal[-i] = value % 10
  return subsignal

# NOTE: I didn't end up using any of this math for the final solution
# (because computing the coefficients was inefficient), but I wanted to
# save it for posterity.

# The pattern for each digit of the second half of the end signal (all mod 10):
#   s[-1] = c_1 * orig[-1]
#   s[-2] = c_1 * orig[-2] + c_2 * orig[-1]
#   s[-3] = c_1 * orig[-3] + c_2 * orig[-2] + c_3 * orig[-1]
#   s[-4] = c_1 * orig[-4] + c_2 * orig[-3] + c_3 * orig[-2] + c_4 * orig[-1]
# etc.
#
# Coefficients (n is the number of phases, 100):
#   c_1 = 1
#   c_2 = n
#   c_3 = n * (n + 1) / 2
#   c_4 = n * (n + 1) * (n + 2) / 6
#   c_5 = n * (n + 1) * (n + 2) * (n + 3) / 24
#
# In general:
#   c_i = n * (n + 1) * ... * (n + (i - 2)) / (1 * 2 * ... * (i - 1))
#
# Test code:
#   print('-5d:', signal[-5], (origSignal[-5] + n * origSignal[-4] + ((n * (n + 1)) // 2) * origSignal[-3] + ((n * (n + 1) * (n + 2)) // 6) * origSignal[-2] + ((n * (n + 1) * (n + 2) * (n + 3)) // 24) * origSignal[-1]) % 10)
#   print('-4d:', signal[-4], (origSignal[-4] + n * origSignal[-3] + ((n * (n + 1)) // 2) * origSignal[-2] + ((n * (n + 1) * (n + 2)) // 6) * origSignal[-1]) % 10)
#   print('-3d:', signal[-3], (origSignal[-3] + n * origSignal[-2] + ((n * (n + 1)) // 2) * origSignal[-1]) % 10)
#   print('-2d:', signal[-2], (origSignal[-2] + n * origSignal[-1]) % 10)
#   assert signal[-1] == origSignal[-1], 'last digit of signal should not change'

def part1() -> None:
  print('input length:', len(input))
  signal = list(map(int, input))
  pattern = [0, 1, 0, -1]
  n = 100
  for _ in range(n):
    signal = onePhase(signal, pattern)

  assert signal[-1] == int(input[-1]), 'last digit of signal should not change'
  print(''.join([str(s) for s in signal[:8]]))

def part2() -> None:
  print('input length:', len(input))
  signal = list(map(int, input))
  n = 100
  mul = 10000

  skip = int(''.join(str(s) for s in signal[:7]))
  print('to skip:', skip)
  fromEnd = len(signal) * mul - skip
  assert fromEnd <= len(signal) * 10000 // 2, 'can only process second half'
  print('from end:', fromEnd)

  endSignal = computeFFTFromEnd(signal * mul, n, fromEnd)
  print('ans len:', len(endSignal))
  print(''.join([str(x) for x in endSignal[:8]]))

part2()
