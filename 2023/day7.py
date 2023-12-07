from collections import defaultdict
from enum import IntEnum
from functools import cmp_to_key

input = open('day7.txt').read().splitlines()

# Explicitly ordered so that higher valued hands have a higher value.
class CardType(IntEnum):
  HIGH_CARD = 1
  ONE_PAIR = 2
  TWO_PAIR = 3
  THREE_OF_A_KIND = 4
  FULL_HOUSE = 5
  FOUR_OF_A_KIND = 6
  FIVE_OF_A_KIND = 7

# R is for Joker
CardOrder = \
  ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'R']

def assertCard(card: str) -> None:
  assert len(card) == 5, 'bad card: %s' % card

def getCardType(card: str) -> CardType:
  assertCard(card)
  d: dict[str, int] = defaultdict(int)
  for c in card:
    d[c] += 1
  sortedValues = sorted(d.values(), reverse=True)
  match sortedValues[0]:
    case 5:
      return CardType.FIVE_OF_A_KIND
    case 4:
      return CardType.FOUR_OF_A_KIND
    case 3:
      if sortedValues[1] == 2:
        return CardType.FULL_HOUSE
      else:
        return CardType.THREE_OF_A_KIND
    case 2:
      if sortedValues[1] == 2:
        return CardType.TWO_PAIR
      else:
        return CardType.ONE_PAIR
    case 1:
      return CardType.HIGH_CARD
    case _:
      assert False, 'bad card type: %s' % card

# Recursively find all possible cards, taking Jokers into account.
def getPossibleCards(card: str, i: int) -> list[str]:
  assertCard(card)
  assert 0 <= i <= 5, 'bad index: %d' % i
  if i == 5:
    return [card]

  if 'R' not in card:
    return [card]

  char = card[i]
  if char != 'R':
    # This isn't a Joker. Move to the next value.
    return getPossibleCards(card, i + 1)

  results = []
  for v in CardOrder:
    if v == 'R':
      # Don't replace R with R.
      continue
    if v not in card:
      # Optimization: don't bother trying values that don't appear
      # elsewhere in the card.
      continue
    # Replace the Joker with another value.
    newCard = card[0:i] + v + card[i + 1:5]
    results.extend(getPossibleCards(newCard, i + 1))
  return results

def getBestCardType(card: str) -> CardType:
  assertCard(card)
  if card == 'RRRRR':
    # Special-case this to make my life easier.
    return CardType.FIVE_OF_A_KIND

  if 'R' not in card:
    # No Jokers. Life if simple.
    return getCardType(card)

  possibleCards = getPossibleCards(card, 0)
  return max([getCardType(c) for c in possibleCards])

def compareCards(c1: str, c2: str) -> int:
  assertCard(c1)
  assertCard(c2)
  t1, t2 = getBestCardType(c1), getBestCardType(c2)
  if t1 > t2:
    # c1 is better
    return 1
  elif t2 > t1:
    # c2 is better
    return -1

  for i in range(5):
    assert c1[i] in CardOrder, 'bad card value: %s' % c1[i]
    assert c2[i] in CardOrder, 'bad card value: %s' % c2[i]
    i1 = CardOrder.index(c1[i])
    i2 = CardOrder.index(c2[i])
    if i1 < i2:
      # c1 is better
      return 1
    elif i2 < i1:
      # c2 is better
      return -1
  assert False, 'equal cards: %s, %s' % (c1, c2)

def compareCardBids(cb1: tuple[str, int], cb2: tuple[str, int]) -> int:
  return compareCards(cb1[0], cb2[0])

def computeWinnings(cardBids: list[tuple[str, int]]) -> int:
  sortedCardBids = sorted(cardBids, key=cmp_to_key(compareCardBids))
  print(sortedCardBids)

  return \
    sum([(i + 1) * sortedCardBids[i][1] for i in range(len(sortedCardBids))])

def part1():
  print('num cards:', len(input))

  cardBids = []
  for line in input:
    card, bid = line.split()
    bid = int(bid)
    cardBids.append((card, bid))
  print(cardBids)

  print(computeWinnings(cardBids))

def part2():
  print('num cards:', len(input))

  cardBids = []
  for line in input:
    card, bid = line.split()
    # Jokers!
    card = card.replace('J', 'R')
    bid = int(bid)
    cardBids.append((card, bid))

  print(computeWinnings(cardBids))

part2()
