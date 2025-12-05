data = open('day5.txt').read().splitlines()

def parse() -> tuple[list[range], list[int]]:
  ranges = []
  ingredients = []
  for line in data:
    if line == '':
      continue
    if '-' in line:
      v1, v2 = map(int, line.split('-'))
      ranges.append(range(v1, v2))
    else:
      ingredients.append(int(line))

  return ranges, ingredients

def isFresh(ranges: list[range], ingredient: int) -> bool:
  return any((r.start <= ingredient <= r.stop) for r in ranges)

def part1() -> None:
  ranges, ingredients = parse()
  print('data:', len(ranges), len(ingredients))

  ans = sum(1 if isFresh(ranges, i) else 0 for i in ingredients)
  print(ans)

part1()
