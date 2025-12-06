from common.ranges import Range, mergeRanges

data = open('day5.txt').read().splitlines()

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

def part2() -> None:
  ranges, _ = parse()
  print('data:', len(ranges))

  ans = sum((e - s + 1) for (s, e) in mergeRanges(ranges))
  print(ans)

part2()
