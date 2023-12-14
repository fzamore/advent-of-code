from functools import cache

input = open('day12.txt').read().splitlines()

def parseLine(line: str) -> tuple[str, list[int]]:
  v = line.split()
  return v[0], list(map(int, v[1].split(',')))

# Returns whether the given value can be placed at the beginning of the
# given string.
def canPlaceValueAtStart(s: str, value: int) -> bool:
  if value > len(s):
    # Value would extend past the end of the string.
    return False

  if s.count('.', 0, value) > 0:
    # There is at least one ground value within the length of the value,
    # so it is impossible to place.
    return False

  if value < len(s) and s[value] == '#':
    # No space on the right.
    return False

  return True

# Count the number of ways the given values can be placed within the given
# string. This needs to be memoized or it won't complete in a reasonable
# amount of time.
@cache
def countWays(s: str, values: tuple[int]) -> int:
  if len(values) == 0:
    # Placing no values is a single valid way if the string contains no #
    # characters.
    return 1 if '#' not in s else 0

  result = 0
  value = values[0]
  for i in range(len(s)):
    sub = s[i:]
    if canPlaceValueAtStart(sub, value):
      # Chop off the portion where the value was placed, plus one
      # character to account for the space.
      v = countWays(sub[value + 1:], values[1:])
      result += v

    if s[i] == '#':
      # If a value had to be placed here, do not look for additional
      # places to put this value.
      return result
  return result

def part1():
  result = 0
  for line in input:
    s, values = parseLine(line)
    print(s, values)

    r = countWays(s, tuple(values))
    print(r)
    print()
    result += r

  print(result)

def part2():
  mul = 5

  result = 0
  for line in input:
    s, values = parseLine(line)
    print(s, values)

    s = ((s + '?') * mul)[:-1]
    values = values * mul
    r = countWays(s, tuple(values))
    print(r)
    print()
    result += r

  print(result)

part2()
