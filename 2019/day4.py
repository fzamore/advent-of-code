v1, v2 = map(int, open('day4.txt').read().split('-'))

def isValid(n: int) -> bool:
  ns = str(n)
  if len(ns) != 6:
    return False

  lastD = -1
  hasDouble = False
  for c in ns:
    d = int(c)
    if d < lastD:
      return False
    if d == lastD:
      hasDouble = True
    lastD = d

  return hasDouble

def part1():
  print('values:', v1, v2)
  ans = 0
  for r in range(v1, v2 + 1):
    if isValid(r):
      ans += 1
  print(ans)

part1()
