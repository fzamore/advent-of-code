from collections import namedtuple

input = open('day4.txt').read().splitlines()

Card = namedtuple('Card', ['id', 'winningNumbers', 'myNumbers'])

def parseLine(line: str) -> Card:
  cardL = line.split(': ')
  id = int(cardL[0].split()[1])
  winningNumbersS, myNumbersS = cardL[1].split(' | ')
  winningNumbers = list(map(int, winningNumbersS.split()))
  myNumbers = list(map(int, myNumbersS.split()))
  return Card(id, winningNumbers, myNumbers)

def part1():
  cards = [parseLine(line) for line in input]
  print(cards)
  print(len(cards))

  sum = 0
  for card in cards:
    s = set(card.winningNumbers)
    matches = [n for n in card.myNumbers if n in s]
    print(card.id, len(matches))
    if len(matches) > 0:
      sum += pow(2, len(matches) - 1)
  print(sum)

part1()
