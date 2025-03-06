input = open('day7.txt').read().splitlines()

def isTlsMatch(s: str, i: int) -> bool:
  if i + 4 > len(s):
    return False

  # mypy is dumb. string unpacking should be allowed.
  # a, b, c, d = s[i:i + 4]
  a, b, c, d = s[i], s[i + 1], s[i + 2], s[i + 3]
  if a == b or c == d:
    return False

  return a == d and b == c

def hasTls(s: str) -> bool:
  assert s.index('[') > 0, 'string must have brackets'

  foundMatchOutsideBracket = False
  inBracket = False
  for i, ch in enumerate(s):
    if ch == '[':
      assert not inBracket, 'brackets cannot be nested'
      inBracket = True
    if ch == ']':
      assert inBracket, 'mismatched brackets'
      inBracket = False

    if isTlsMatch(s, i):
      if inBracket:
        return False
      else:
        foundMatchOutsideBracket = True

  return foundMatchOutsideBracket

def isSslMatch(s: str, i: int) -> bool:
  if i + 3 > len(s):
    return False

  # Again, mypy is dumb re: disallowing string unpacking.
  # a, b, c = s[i:i + 3]
  a, b, c = s[i], s[i + 1], s[i + 2]
  if '[' in (a, b, c) or ']' in (a, b, c):
    return False
  return a != b and a == c

def hasMatchingSsl(s: str, start: int, a: str, b: str, brackets: list[bool]) -> bool:
  assert len(a) == 1 and len(b) == 1, 'a and b should be single chars'
  startInBracket = brackets[start]
  assert startInBracket is not None, 'start character cannot be [ or ]'
  for i in range(start, len(s)):
    if isSslMatch(s, i) and brackets[i] != startInBracket:
      assert s[i] == s[i + 2], 'bad ssl match'
      if s[i] == b and s[i + 1] == a:
        return True
  return False

def hasSsl(s: str, brackets: list[bool]) -> bool:
  for i in range(len(s)):
    if isSslMatch(s, i):
      a, b = s[i], s[i + 1]
      if hasMatchingSsl(s, i, a, b, brackets):
        return True
  return False

def part1() -> None:
  ans = sum([1 for line in input if hasTls(line)])
  print(ans)

def part2() -> None:
  print('input:', len(input))

  ans = 0
  for line in input:
    # Compute whether each char is inside or outside bracket.
    inBracket = False
    brackets: list[bool] = []
    for ch in line:
      if ch in ['[', ']']:
        assert inBracket != (ch == '['), 'brackets cannot be nested or mismatched'
        inBracket = ch == '['
        # By convention, consider the bracket characters themselves to be
        # not within a bracket.
        brackets.append(False)
      else:
        brackets.append(inBracket)

    if hasSsl(line, brackets):
      ans += 1

  print(ans)

part2()
