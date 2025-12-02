from typing import Iterable

data = open('day1.txt').read().splitlines()

def parse() -> Iterable[int]:
  for line in data:
    r = -1 if line[0] == 'L' else 1
    v = int(line[1:])
    assert v != 0, 'no zeroes allowed'
    yield r * v

def doesPassZeroInPartialLoop(dial: int, v: int, m: int) -> bool:
  newdial = (dial + v) % m
  assert newdial != dial, 'loops starting and ending at zero are not allowed'
  if v > 0:
    # Going right is simple; we pass zero in partial loop if we end up lower than we started.
    return newdial < dial

  if newdial == 0:
    # We ended up at zero. Count it.
    return True

  # When going left, if we end up with a higher number than we started
  # with, we passed zero in a partial loop. One exception to this is if
  # we started at zero, would always trigger this condition.
  return newdial > dial and dial != 0

def part1() -> None:
  dial = 50
  m = 100
  ans = 0
  for v in parse():
    dial = (dial + v) % m
    ans += 1 if dial == 0 else 0
  print(ans)

def part2() -> None:
  dial = 50
  m = 100
  ans = 0
  for v in parse():
    # Full loops.
    ans += abs(v) // m
    # Partial loop.
    ans += 1 if doesPassZeroInPartialLoop(dial, v, m) else 0
    dial = (dial + v) % m
  print(ans)

part2()
