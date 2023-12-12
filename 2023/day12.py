from itertools import combinations, permutations


input = open('day12.txt').read().splitlines()

def parseLine(line: str) -> tuple[str, list[int]]:
  v = line.split()
  return v[0], list(map(int, v[1].split(',')))

def canPlaceValue(s: list[str], value: int, index: int) -> bool:
  if index + value > len(s):
    # Value would extend past the end of the string.
    return False

  for i in range(index, index + value):
    if s[i] not in ['#', '?']:
      return False
  if index > 0 and s[index - 1] not in ['.', '?']:
    # No space on the left.
    return False
  if index + value < len(s) and s[index + value] not in ['.', '?']:
    # No space on the right.
    return False
  return True

# Finds the ways to place the value at valuesIndex, starting at startI
# position in the input list / string. Results are put into the ways set.
def findWaysForValue(
  s: list[str],
  values: list[int],
  valuesIndex: int,
  startI: int,
  ways: set[str],
) -> None:
  if valuesIndex == len(values):
    if '#' not in s[startI:]:
      # Make sure we don't have any "#" characters left over.
      r = ''.join([str(x) for x in s])
      r = r.replace('?', '.')
      ways.add(r)
    return

  value = values[valuesIndex]
  for i in range(startI, len(s)):
    if canPlaceValue(s, value, i):
      # Copy the list
      s2 = s.copy()
      # Place the value
      for j in range(value):
        s2[i + j] = '#'
      findWaysForValue(s2, values, valuesIndex + 1, i + value + 1, ways)
    if s[i] == '#':
      # If a value had to be placed here, do not look for additional
      # places to put this value.
      return

def verifyWay(s: str, way: str, values: list[int]) -> None:
  assert len(way) == len(s)
  for i in range(len(s)):
    if way[i] == '.':
      assert s[i] in ['.', '?'], 'bad ground'
    elif way[i] == '#':
      assert s[i] in ['#', '?'], 'bad number'
    else:
      assert False, 'bad character'

  toCheck = [x for x in way.split('.') if x != '']
  assert len(toCheck) == len(values), \
    'bad values: %s %s || %s' % (values, s, way)
  for i in range(len(values)):
    assert len(toCheck[i]) == values[i], 'bad value'

def part1():
  result = 0
  for line in input:
    s, values = parseLine(line)
    print(s, values)
    ways = set()
    findWaysForValue(list(s), values, 0, 0, ways)
    [verifyWay(s, x, values) for x in ways]
    [print(x) for x in ways]
    print(len(ways))
    print()
    result += len(ways)

  print(result)

part1()
