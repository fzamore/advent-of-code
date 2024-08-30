from collections import deque

input = open('day10.txt').read().strip()

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

def part1() -> None:
  seq = list(range(256))
  lengths = list(map(int, input.split(',')))
  print('lengths:', lengths)

  seq, _, _ = oneRound(seq, lengths)
  print(seq[0] * seq[1])

def part2() -> None:
  seq = list(range(256))

  lengths = [ord(c) for c in input]
  lengths.extend([17, 31, 73, 47, 23])
  print('lengths:', lengths)

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
  print(''.join(hexChars))

part2()
