from collections import Counter

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

  onLookup: dict[int, int] = Counter()
  offLookup: dict[int, int] = Counter()
  for rs, re in ranges:
    onLookup[rs] += 1
    offLookup[re] += 1

  # Iterate through the start and stop values of all ranges in increasing
  # order. Maintain a polarity integer that tracks whether or not we are
  # currently within a range (positive means within a range, zero means
  # not; cannot be negative). At each value, determine if it's an "on" or
  # "off". If this "off" value closes a range, add the count so far. We
  # need to take into account that each value could be present in multiple
  # ranges, as either or both of "on" or "off".

  polarity = 0 # Whether we are currently in a range.
  onValue = None # Value that turned on the current range.
  count = 0
  for k in sorted(list(onLookup.keys()) + list(offLookup.keys())):
    assert k in onLookup or k in offLookup, 'missing range'
    assert polarity >= 0, 'bad polarity'

    while onLookup[k] > 0:
      onLookup[k] -= 1
      print('on:', k)
      polarity += 1
      if onValue is None:
        onValue = k

    while offLookup[k] > 0:
      offLookup[k] -= 1
      print('off:', k)
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
