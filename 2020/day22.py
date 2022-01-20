from common.io import readfile
from collections import defaultdict

def serialize(decks):
  return \
    ','.join([str(x) for x in decks[1]]) + \
    ':' + \
    ','.join([str(x) for x in decks[2]])

def computeWinnerAndUpdateDecks(decks, p1, p2):
  assert p1 != p2, 'equal top cards: %d %d' % (p1, p2)
  if p1 > p2:
    decks[1].append(p1)
    decks[1].append(p2)
  else:
    decks[2].append(p2)
    decks[2].append(p1)

def playRound(decks):
  computeWinnerAndUpdateDecks(decks, decks[1].pop(0), decks[2].pop(0))

def playGame2(decks):
  p1 = decks[1]
  p2 = decks[2]
  #print('playing game %d, %s, %s' % (gameNum, p1, p2))

  prevGames = set()
  while len(p1) > 0 and len(p2) > 0:    
    serialized = serialize(decks)
    if serialized in prevGames:
      # prevent infinite recursion
      return 1
    prevGames.add(serialized)

    p1c = p1.pop(0)
    p2c = p2.pop(0)
    if p1c > len(p1) or p2c > len(p2):
      # normal game
      computeWinnerAndUpdateDecks(decks, p1c, p2c)
    else:
      # recursive subgame
      subdecks = {
        1: p1[0:p1c],
        2: p2[0:p2c],
      }
      subwinner = playGame2(subdecks)
      winningCard = p1c if subwinner == 1 else p2c
      losingCard = p1c if subwinner == 2 else p2c
      decks[subwinner].append(winningCard)
      decks[subwinner].append(losingCard)
    
  winner = 1 if len(p2) == 0 else 2
  return winner

def computeScore(deck):
   # reverse the deck to compute the score
  cards = deck[::-1]
  score = 0
  mul = 1
  for c in cards:
    score += c * mul
    mul += 1
  return score

def part1():
  player = None
  decks = defaultdict(list)
  for line in readfile('day22.txt'):    
    if line == '':
      continue
    if line[0:7] == 'Player ':
      player = int(line[7])
      continue
    assert player != None, 'have not found player yet'
    decks[player].append(int(line))
  print(decks)
  assert len(decks[1]) == len(decks[2]), 'mismatched deck lengths'
  deckLength = len(decks[1])
  print('deck length', deckLength)

  i = 0
  while len(decks[1]) > 0 and len(decks[2]) > 0:
    playRound(decks)
    i += 1
  print('game over after round:', i)
  print(decks)
  cards = decks[1] if len(decks[2]) == 0 else decks[2]
  assert len(cards) == deckLength * 2, 'bad winning hand length'
  print(computeScore(cards))

def part2():
  player = None
  decks = defaultdict(list)
  for line in readfile('day22.txt'):    
    if line == '':
      continue
    if line[0:7] == 'Player ':
      player = int(line[7])
      continue
    assert player != None, 'have not found player yet'
    decks[player].append(int(line))
  print('deck lengths', len(decks[1]), len(decks[2]))

  winner = playGame2(decks)
  print()
  print('winner: %d. final hand: %s' % (winner, decks[winner]))
  
  print(computeScore(decks[winner]))

part2()
