from collections import Counter
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
  c = Counter(card)
  sortedValues = sorted(c.values(), reverse=True)
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


def getBestCardType(card: str) -> CardType:
  assertCard(card)
  if card == 'RRRRR':
    # Special-case this to make my life easier.
    return CardType.FIVE_OF_A_KIND

  if 'R' not in card:
    # No Jokers. Life if simple.
    return getCardType(card)

  # Find the best card type, taking Jokers into account.
  possibleCardTypes = []
  nonJokerValues = set(card) - set('R')
  for v in nonJokerValues:
    # Replace all Jokers with this value. We don't need to replace
    # multiple Jokers with multiple values because replacing all Jokers
    # with a single value will always be better.
    ncard = card.replace('R', v)
    possibleCardTypes.append(getCardType(ncard))
  return max(possibleCardTypes)

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
