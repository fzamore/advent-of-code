data = open('day11.txt').read().rstrip()

def isRun(s: str, i: int) -> bool:
  if i > len(s) - 3:
    return False

  b = ord(s[i])
  return ord(s[i + 1]) == b + 1 and ord(s[i + 2]) == b + 2

def hasRun(s: str) -> bool:
  return any([isRun(s, i) for i in range(len(s))])

def hasTwoDoubles(s: str) -> bool:
  doubleChar = ''
  for i in range(len(s) - 1):
    if s[i] == s[i + 1]:
      if doubleChar != '' and s[i] != doubleChar:
        return True
      doubleChar = s[i]
  return False

def isValid(s: str) -> bool:
  assert len(s) == 8, 'bad string len'
  if not hasRun(s):
    return False

  if any([ch in s for ch in ['i', 'o', 'l']]):
    return False

  if not hasTwoDoubles(s):
    return False

  return True

def incr(s: str) -> str:
  assert len(s) == 8
  newChars: list[str] = []

  # Optimization: if one of the banned characters exists in the string,
  # fast-forward to the next string without the banned character.
  for i in range(len(s)):
    ch = s[i]
    if ch in ['l', 'o', 'i']:
      # Increment the banned character and put all a's after that.
      return s[:i] + chr(ord(ch) + 1) + ('a' * (len(s) - i - 1))

  # Handle overflow.
  i = 7
  while i >= 0:
    ch = s[i]
    if ch != 'z':
      newChars.insert(0, chr(ord(ch) + 1))
      i -= 1
      break
    newChars.insert(0, 'a')
    i -= 1

  while i >= 0:
    newChars.insert(0, s[i])
    i -= 1

  return ''.join(newChars)

def part1() -> None:
  print('input:', data)
  s = data
  while not isValid(s := incr(s)): pass
  print(s)

def part2() -> None:
  print('input:', data)
  s = data
  while not isValid(s := incr(s)): pass
  print('next:', s)
  while not isValid(s := incr(s)): pass
  print(s)

part2()
