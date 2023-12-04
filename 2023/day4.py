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

def part2():
  cards = [parseLine(line) for line in input]
  print(cards)
  print(len(cards))

  cardScores = {}
  cardsInHand = {}
  for card in cards:
    s = set(card.winningNumbers)
    matches = [n for n in card.myNumbers if n in s]
    score = len(matches)
    cardScores[card.id] = score

    cardsInHand[card.id] = 1

  print(cardsInHand)
  print(cardScores)

  maxId = max(cardScores.keys())
  print('maxId:', maxId)
  print()

  # Process cards in order, since card X can only affect cards > X.
  for cardId in range(1, maxId + 1):
    score = cardScores[cardId]
    if score == 0:
      continue
    assert cardId + score <= maxId, 'bad card score'
    for i in range(cardId + 1, cardId + score + 1):
      # For each matching card, add as many copies as we have of the
      # current card.
      cardsInHand[i] += cardsInHand[cardId]

  print(cardsInHand)
  print(sum(cardsInHand.values()))

part2()
