v1, v2 = map(int, open('day4.txt').read().split('-'))

def isValid(n: int, *, part2: bool = False) -> bool:
  ns = str(n)
  if len(ns) != 6:
    return False

  lastD = -1
  hasDouble = False
  i = 0
  while i < len(ns):
    d = int(ns[i])
    if d < lastD:
      return False

    adjCount = 1
    j = i + 1
    while j < len(ns) and int(ns[j]) == d:
      adjCount += 1
      j += 1

    if not hasDouble:
      if part2:
        hasDouble = (adjCount == 2)
      else:
        hasDouble = (adjCount > 1)

    lastD = d
    i = j

  return hasDouble

def part1():
  print('values:', v1, v2)
  ans = 0
  for r in range(v1, v2 + 1):
    if isValid(r):
      ans += 1
  print(ans)

def part2():
  print('values:', v1, v2)
  ans = 0
  for r in range(v1, v2 + 1):
    if isValid(r, part2=True):
      ans += 1
  print(ans)

part2()
