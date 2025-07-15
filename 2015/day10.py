data = open('day10.txt').read().rstrip()

def expand(s: str) -> str:
  assert len(s) > 0, 'bad input str'
  newChars = []
  curChar = s[0]
  curCount = 1
  for ch in s[1:]:
    if ch == curChar:
      curCount += 1
    else:
      newChars.extend([str(curCount), curChar])
      curChar = ch
      curCount = 1
  newChars.extend([str(curCount), curChar])
  return ''.join(newChars)

def computeLen(s: str, n: int) -> int:
  for _ in range(n):
    s = expand(s)
  return len(s)

def part1() -> None:
  print('input:', data)
  print(computeLen(data, 40))

def part2() -> None:
  print('input:', data)
  print(computeLen(data, 50))

part2()
