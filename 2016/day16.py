input = open('day16.txt').read().rstrip()

def dragonSingle(s: str) -> str:
  a, b = s, s[::-1]
  b = ''.join(['0' if c == '1' else '1' for c in b])
  return '%s0%s' % (a, b)

def dragon(s: str, n: int) -> str:
  while len(s) < n:
    s = dragonSingle(s)
  return s[:n]

def checksum(s: str) -> str:
  while len(s) % 2 == 0:
    ns = []
    for i in range(len(s) // 2):
      ns.append('1' if s[2 * i] == s[2 * i + 1] else '0')
    s = ''.join(ns)
  return s

# Stolen from Reddit. Break the input string into an odd number of chunks
# (of largest odd divisor, which implies the chunk size is always even).
# Count the number of 1s in each chunk; if even, append '1' to checksum,
# otherwise, append '0'.
def checksumFast(s: str) -> str:
  assert len(s) % 2 == 0, 'need even string for checksum'

  # Find the number of chunks, which is the largest odd divisor.
  numChunks = len(s)
  while numChunks % 2 == 0:
    numChunks //= 2
  assert len(s) % numChunks == 0, 'chunk count should divide string length'

  chunkSize = len(s) // numChunks
  assert chunkSize % 2 == 0, 'chunk size should always be even'
  print('chunkSize, numChunks:', chunkSize, numChunks)

  r = []
  for i in range(numChunks):
    numOnes = s[chunkSize * i:chunkSize * (i + 1)].count('1')
    r.append('1' if numOnes % 2 == 0 else '0')
  return ''.join(r)

def part1() -> None:
  n = 272
  print('input:', input)
  s = dragon(input, n)
  print('after dragon:', len(s))
  s = checksum(s)
  print(s)

def part2() -> None:
  n = 35651584
  print('input:', input)
  s = dragon(input, n)
  print('after dragon:', len(s))
  s = checksumFast(s)
  print(s)

part2()
