data = open('day16.txt').read().splitlines()

Sue = dict[str, int]
Sues = dict[str, Sue]

def parse() -> Sues:
  sues: Sues = {}
  for line in data:
    k = line.split()[1][:-1]
    sues[k] = {}
    text = ''.join(line.split()[2:])
    for item in text.split(','):
      v = item.split(':')
      sues[k][v[0]] = int(v[1])
  return sues

def getMatchData() -> Sue:
  return {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
  }

def isMatch(sue: Sue) -> bool:
  match = getMatchData()
  return all(sue[k] == match[k] for k in sue)

def isMatch2(sue: Sue) -> bool:
  match = getMatchData()
  for k in sue:
    s = sue[k]
    m = match[k]
    match k:
      case 'cats' | 'trees':
        if s <= m:
          return False
      case 'pomeranians' | 'goldfish':
        if s >= m:
          return False
      case _:
        if s != m:
          return False
  return True

def part1() -> None:
  sues = parse()
  for k in sues:
    if isMatch(sues[k]):
      print('match:', k, sues[k])
      print(k)

def part2() -> None:
  sues = parse()
  for k in sues:
    if isMatch2(sues[k]):
      print('match:', k, sues[k])
      print(k)

part2()
