from common.readfile import readfile

def convertToCanonical(letter: str) -> str:
  return {
    'A': 'R',
    'B': 'P',
    'C': 'S',
    'X': 'R',
    'Y': 'P',
    'Z': 'S',
  }[letter]

def convertToCanonical2(letter: str) -> str:
  return {
    'A': 'R',
    'B': 'P',
    'C': 'S',
    'X': 'lose',
    'Y': 'tie',
    'Z': 'win',
  }[letter]

def getValue(canonical: str) -> int:
  return {
    'R': 1,
    'P': 2,
    'S': 3,
  }[canonical]

def getOutcome(c1: str, c2: str) -> str:
  if c1 == c2:
    return 'tie'

  if c1 == 'R':
    return 'win' if c2 == 'S' else 'loss'
  elif c1 == 'P':
    return 'win' if c2 == 'R' else 'loss'
  else:
    return 'win' if c2 == 'P' else 'loss'

def getScore(c1: str, c2: str) -> int:
  outcome = getOutcome(c1, c2)
  return {'win': 6, 'tie': 3, 'loss': 0}[outcome] + getValue(c1)

def getC1(c2: str, outcome: str) -> str:
  if c2 == 'R':
    return {'win': 'P', 'tie': 'R', 'lose': 'S'}[outcome]
  elif c2 == 'P':
    return {'win': 'S', 'tie': 'P', 'lose': 'R'}[outcome]
  else:
    return {'win': 'R', 'tie': 'S', 'lose': 'P'}[outcome]

def part1():
  total = 0
  for line in readfile('day2.txt'):
    two, one = line.split()
    c1, c2 = convertToCanonical(one), convertToCanonical(two)
    total += getScore(c1, c2)
  print(total)

def part2():
  total = 0
  for line in readfile('day2.txt'):
    two, res = line.split()
    c2, outcome = convertToCanonical2(two), convertToCanonical2(res)
    c1 = getC1(c2, outcome)
    total += getScore(c1, c2)
  print(total)

part2()
