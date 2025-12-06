data = open('day5.txt').read().splitlines()

Range = tuple[int, int]

def parse() -> tuple[list[Range], list[int]]:
  ranges = []
  ingredients = []
  for line in data:
    if line == '':
      continue
    if '-' in line:
      v1, v2 = map(int, line.split('-'))
      assert v2 >= v1, 'bad range spec'
      ranges.append((v1, v2))
    else:
      ingredients.append(int(line))

  return ranges, ingredients

def isOverlapping(r1: Range, r2: Range) -> bool:
  s1, e1 = r1
  s2, e2 = r2
  assert s1 <= e1 and s2 <= e2, 'bad range spec'
  return not (e1 < s2 or e2 < s1)

def mergeRange(ranges: list[Range], rng: Range) -> list[Range]:
  newRanges = []
  rangeToAdd = rng
  for r in ranges:
    if not isOverlapping(r, rangeToAdd):
      # This range does not overlap. Maintain the existing range.
      newRanges.append(r)
      continue

    start, end = rangeToAdd
    s, e = r
    rangeToAdd = (min(s, start), max(e, end))

  newRanges.append(rangeToAdd)
  return newRanges

def mergeRanges(ranges: list[Range]) -> list[Range]:
  mergedRanges: list[Range] = []
  for r in ranges:
    mergedRanges = mergeRange(mergedRanges, r)
  return mergedRanges

def part2() -> None:
  ranges, _ = parse()
  print('data:', len(ranges))

  ans = sum((e - s + 1) for (s, e) in mergeRanges(ranges))
  print(ans)

part2()
