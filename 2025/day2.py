data = open('day2.txt').read()

def isInvalid(v: int) -> bool:
  s = str(v)
  n = len(s)
  if n % 2 == 1:
    return False

  return s[:n//2] == s[n//2:]

def part1() -> None:
  ranges = data.split(',')
  print('ranges:', len(ranges))
  ans = 0
  for rng in ranges:
    start, end = map(int, rng.split('-'))
    ans += sum(i if isInvalid(i) else 0 for i in range(start, end + 1))
  print(ans)

part1()
