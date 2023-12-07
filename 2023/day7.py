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

CardOrder = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

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

def compareCards(c1: str, c2: str) -> int:
  assertCard(c1)
  assertCard(c2)
  t1, t2 = getCardType(c1), getCardType(c2)
  if t1 > t2:
    # c1 is better
    return 1
  elif t2 > t1:
    # c2 is better
    return -1

  for i in range(5):
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

def part1():
  print('num cards:', len(input))

  cardBids = []
  for line in input:
    card, bid = line.split()
    bid = int(bid)
    cardBids.append((card, bid))
  print(cardBids)

  sortedCardBids = sorted(cardBids, key=cmp_to_key(compareCardBids))
  print(sortedCardBids)

  print(
    sum([(i + 1) * sortedCardBids[i][1] for i in range(len(sortedCardBids))]),
  )

part1()
