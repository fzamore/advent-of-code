data = open('day5.txt').read().splitlines()

Range = tuple[int, int]

def parse() -> tuple[set[Range], list[int]]:
  ranges = set()
  ingredients = []
  for line in data:
    if line == '':
      continue
    if '-' in line:
      v1, v2 = map(int, line.split('-'))
      assert v2 >= v1, 'bad range spec'
      ranges.add((v1, v2))
    else:
      ingredients.append(int(line))

  return ranges, ingredients

def isFresh(ranges: set[Range], ingredient: int) -> bool:
  return any((rs <= ingredient <= re) for (rs, re) in ranges)

def part1() -> None:
  ranges, ingredients = parse()
  print('data:', len(ranges), len(ingredients))

  ans = sum(1 if isFresh(ranges, i) else 0 for i in ingredients)
  print(ans)

def part2() -> None:
  ranges, _ = parse()
  print('data:', len(ranges))

  keys = []
  for rs, re in ranges:
    keys.append((rs, True))
    keys.append((re, False))

  # Iterate through the start and stop values of all ranges in increasing
  # order. Maintain a polarity integer that tracks whether or not we are
  # currently within a range (positive means within a range, zero means
  # not; cannot be negative). At each value, determine if it's a start or
  # end. If this end value closes a range, add the count so far. If a
  # value is both a start and end, we need to process the starts first.

  polarity = 0 # Whether we are currently in a range.
  startValue = None # Value that started the current range.
  count = 0

  # Sort the keys, but break ties by always putting starts before ends.
  sortedKeys = sorted(keys, key=lambda x: (x[0], (1 if x[1] else 2)))
  for k, isStart in sortedKeys:
    assert polarity >= 0, 'bad polarity'

    if isStart:
      polarity += 1
      if startValue is None:
        startValue = k
    else:
      polarity -= 1
      if polarity == 0:
        # This end value closes a range. Add the count.
        assert startValue is not None, 'startValue not set'
        delta = k - startValue + 1
        print('adding:', k, startValue, delta)
        count += delta
        # Reset the start value.
        startValue = None

  print(count)

part2()
