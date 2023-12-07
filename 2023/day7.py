from collections import Counter
from enum import IntEnum

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

# Function to pass to key= in sorted().
def cardKey(card: str) -> tuple[int, list[int]]:
  cardType = getBestCardType(card)
  # Use a list of CardOrder indices as a tiebreaker when the card type is
  # the same (since lists get pairwise compared by sorted()).
  tiebreaker = [len(CardOrder) - CardOrder.index(c) for c in card]
  return cardType, tiebreaker

def computeWinnings(cardBids: list[tuple[str, int]]) -> int:
  sortedCardBids = sorted(cardBids, key=lambda cb: cardKey(cb[0]))
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
