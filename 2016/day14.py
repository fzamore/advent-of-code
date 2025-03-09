from typing import Optional
from common.md5 import md5hash
from functools import cache

input = open('day14.txt').read().rstrip()

@cache
def hash(s: str, i: int, k: int):
  h = '%s%d' %(s, i)
  for _ in range(k + 1):
    h = md5hash(h)
  return h

def getTripletChar(n: int, k: int) -> Optional[str]:
  h = hash(input, n, k)
  for i in range(len(h) - 2):
    if h[i] == h[i + 1] == h[i + 2]:
      return h[i]
  return None

def hasQuint(n: int, ch: str, k: int) -> bool:
  assert len(ch) == 1, 'bad char input'
  h = hash(input, n, k)
  return h.find(ch * 5) != -1

def isKey(i: int, k: int) -> bool:
  ch = getTripletChar(i, k)
  if ch is None:
    return False

  c = 1000
  for n in range(c):
    if hasQuint(i + 1 + n, ch, k):
      return True
  return False

def findNthKey(n: int, k: int = 0) -> int:
  i = 0
  keys = 0
  while True:
    if isKey(i, k):
      keys += 1
      print('key:', keys, i)
      if keys == n:
        return i
    i += 1

def part1() -> None:
  print(findNthKey(64))

def part2() -> None:
  print(findNthKey(64, 2016))

part2()
