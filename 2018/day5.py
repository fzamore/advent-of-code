from collections import deque
from typing import Iterable

input = open('day5.txt').read()[:-1]

def isMatch(c1, c2: str) -> bool:
  if c1.islower():
    return c2.isupper() and c2.lower() == c1
  elif c1.isupper():
    return c2.islower() and c2.upper() == c1
  else:
    assert False, 'bad input'

def react(s: Iterable[str]):
  stack: deque[str] = deque()
  for c in s:
    if len(stack) > 0 and isMatch(c, stack[-1]):
      stack.pop()
    else:
      stack.append(c)

  for i in range(len(stack) - 1):
    assert not isMatch(stack[i], stack[i + 1]), 'bad stack'

  return ''.join(stack)

def removeChars(s: Iterable[str], chars: set[str]) -> list[str]:
  return [c for c in s if c not in chars]

def part1() -> None:
  print('len:', len(input))

  ans = react(input)
  print(ans)
  print(len(ans))

def part2() -> None:
  print('len:', len(input))
  ans = len(input)
  for cdigit in range(ord('a'), ord('z') + 1):
    c = chr(cdigit)
    s = removeChars(input, {c, c.upper()})
    ans = min(ans, len(react(s)))
  print(ans)

part2()
