from collections import deque

input = int(open('day19.txt').read().rstrip())

# We don't care how many presents each elf has; we only care about whether
# each elf is in the circle or not. We also don't care about which elf is
# doing the stealing; we only care about which elf is being stolen from
# (i.e., eliminated). The front of the deque always represents the next
# elf to be eliminated.

def part1() -> None:
  print('input:', input)

  # This starts at elf zero (we assume zero-indexed).
  d = deque(range(input))
  # Eliminate the elf to its left.
  d.rotate(-1)
  while len(d) > 1:
    d.popleft()
    d.rotate(-1)
  assert len(d) == 1, 'bad deque management'
  print(d.pop() + 1)

def part2() -> None:
  print('input:', input)

  d = deque(range(input))
  # Start by eliminating the elf across the circle.
  d.rotate(-(len(d) // 2))
  while len(d) > 1:
    d.popleft()
    if len(d) % 2 == 0:
      # If there are an even number of elves left, we have to rotate one
      # more spot.
      d.rotate(-1)
  assert len(d) == 1, 'bad deque management'
  print(d.pop() + 1)

part2()
