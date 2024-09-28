from collections import deque
from typing import Iterator
from common.arraygrid import ArrayGrid
from common.graphtraversal import getConnectedComponents

input = open('day14.txt').read().strip()

Seq = list[int]

def oneRound(
  seq: Seq,
  lengths: list[int],
  pos: int = 0,
  skip: int = 0,
) -> tuple[Seq, int, int]:
  n = 256
  data = deque(seq)

  # Rotate the deque so that we're always reversing the sublist at the
  # beginning of the deque.
  data.rotate(-pos)

  for length in lengths:
    assert length <= n, 'bad length in list'
    sublist = []
    for _ in range(length):
      sublist.append(data.popleft())
    for e in sublist:
      data.appendleft(e)

    rot = length + skip
    data.rotate(-rot)

    # Update the position so we can rotate the sequence correctly at the end of the round.
    pos = (pos + rot) % n
    skip += 1

  # Rotate the sequence back into the correct position.
  data.rotate(pos)
  return list(data), pos, skip

def knothash(s: str) -> str:
  seq = list(range(256))

  lengths = [ord(c) for c in s]
  lengths.extend([17, 31, 73, 47, 23])

  pos, skip = 0, 0
  for _ in range(64):
    seq, pos, skip = oneRound(seq, lengths, pos, skip)

  hexChars = []
  for i in range(16):
    xor = 0
    for j in range(16):
      xor ^= seq[i * 16 + j]
    hexChars.append('%02x' % xor)

  assert len(hexChars) == 16, 'should be 16 hex chars'
  return ''.join(hexChars)

def initGrid(n: int) -> ArrayGrid:
  grid = ArrayGrid(n, n)
  for row in range(n):
    s = '%s-%d' %(input, row)
    h = knothash(s)
    bitStr = bin(int(h, 16))[2:].zfill(n)
    assert len(bitStr) == n
    for col, c in enumerate(bitStr):
      if c == '1':
        grid.setValue(col, row, '#')
  return grid

def part1() -> None:
  n = 128
  c = 0
  for row in range(n):
    s = '%s-%d' %(input, row)
    h = knothash(s)
    # Python is a cheat code.
    c += int(h, 16).bit_count()
  print(c)

def part2() -> None:
  n = 128
  grid = initGrid(n)
  allNodes = []
  for row in range(n):
    for col in range(n):
      if grid.hasValue(col, row):
        allNodes.append((col, row))
  print('cells:', len(allNodes))

  def getAdj(pos: tuple[int, int]) -> Iterator[tuple[int, int]]:
    x, y = pos
    for nx, ny in grid.getAdjacentCoords(x, y, includeDiagonals=False):
      if grid.hasValue(nx, ny):
        yield nx, ny
  connectedComponents = getConnectedComponents(allNodes, getAdj)
  print(len(connectedComponents))

part2()
