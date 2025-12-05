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
  # not; cannot be negative). At each value, determine if it's an "on" or
  # "off". If this "off" value closes a range, add the count so far. If a
  # value is both an "on" and "off", we need to process the "on"s first.

  polarity = 0 # Whether we are currently in a range.
  onValue = None # Value that turned on the current range.
  count = 0

  # Sort the keys, but break ties by always putting on's before off's.
  sortedKeys = sorted(keys, key=lambda x: (x[0], (1 if x[1] else 2)))
  for k, isOn in sortedKeys:
    assert polarity >= 0, 'bad polarity'

    if isOn:
      polarity += 1
      if onValue is None:
        onValue = k
    else:
      polarity -= 1
      if polarity == 0:
        # This "off" value closes a range. Add the count.
        assert onValue is not None, 'onValue not set'
        delta = k - onValue + 1
        print('adding:', k, onValue, delta)
        count += delta
        onValue = None

  print(count)

part2()
