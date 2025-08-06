from collections import namedtuple
from typing import Iterable
from common.shortestpath import dijkstra
from common.ints import ints

data = open('day22.txt').read().splitlines()

Player = namedtuple('Player', ['hitpoints', 'armor', 'mana', 'shield','poison', 'recharge'], defaults=(0, 0, 0, 0, 0, 0))
Boss = namedtuple('Boss', ['hitpoints', 'damage'], defaults=(0, 0))
Node = tuple[Player, Boss, bool] # isPlayerTurn

def parseBoss() -> Boss:
  return Boss(hitpoints=ints(data[0])[0], damage=ints(data[1])[0])

def handleEffects(player: Player, boss: Boss) -> tuple[Player, Boss]:
  hitpoints, armor, mana, shield, poison, recharge = player
  bossHitpoints, bossDamage = boss
  if shield > 0:
    if shield == 6:
      armor += 7
    if shield == 1:
      armor -= 7
    shield -= 1
  if poison > 0:
    poison -= 1
    bossHitpoints -= 3
  if recharge > 0:
    recharge -= 1
    mana += 101

  return Player(hitpoints, armor, mana, shield, poison, recharge), Boss(bossHitpoints, bossDamage)

def canPlayerAttack(player: Player, costs: dict[str, int], spell: str) -> bool:
  assert player.shield >= 0 and player.poison >= 0 and player.recharge >= 0, 'bad effects'
  if player.mana < costs[spell]:
    return False

  match spell:
    case 'missile' | 'drain':
      return True
    case 'shield':
      return player.shield == 0
    case 'poison':
      return player.poison == 0
    case 'recharge':
      return player.recharge == 0
    case _:
      assert False, 'bad spell'

def playerAttack(player: Player, boss: Boss, costs: dict[str, int], spell: str) -> tuple[Player, Boss]:
  assert canPlayerAttack(player, costs, spell), 'player cannot attack'

  hitpoints, _, mana, shield, poison, recharge = player
  bossHitpoints, _ = boss

  assert mana >= costs[spell], 'not enough mana'
  mana -= costs[spell]

  match spell:
    case 'missile':
      bossHitpoints -= 4
    case 'drain':
      bossHitpoints -= 2
      hitpoints += 2
    case 'shield':
      assert shield == 0, 'effect should have already been drained'
      shield = 6
    case 'poison':
      assert poison == 0, 'effect should have already been drained'
      poison = 6
    case 'recharge':
      assert recharge == 0, 'effect should have already been drained'
      recharge = 5
    case _:
      assert False, 'bad spell'

  return Player(hitpoints, player.armor, mana, shield, poison, recharge), boss._replace(hitpoints=bossHitpoints)

def bossAttack(player: Player, boss: Boss) -> Player:
  damage = max(1, boss.damage - player.armor)
  return player._replace(hitpoints=player.hitpoints - damage)

def getAdjacent(node: Node, *, hardMode: bool = False) -> Iterable[tuple[Node, int]]:
  player, boss, isPlayerTurn = node
  costs = {
    'missile': 53,
    'drain': 73,
    'shield': 113,
    'poison': 173,
    'recharge': 229,
  }

  if player.hitpoints <= 0:
    # Dead player.
    return []

  assert boss[0] > 0, 'boss should be alive'

  for spell in costs:
    adjplayer, adjboss = player, boss
    if isPlayerTurn and hardMode:
      adjplayer = player._replace(hitpoints=player.hitpoints - 1)

    adjplayer, adjboss = handleEffects(adjplayer, adjboss)
    if adjboss.hitpoints <= 0:
      # Boss died from effects.
      yield (adjplayer, adjboss, not isPlayerTurn), 0
      continue

    if isPlayerTurn and canPlayerAttack(adjplayer, costs, spell):
      # The player attacks.
      adjplayer, adjboss = playerAttack(adjplayer, adjboss, costs, spell)
      yield (adjplayer, adjboss, not isPlayerTurn), costs[spell]

    if not isPlayerTurn:
      # The boss attacks.
      adjplayer = bossAttack(adjplayer, adjboss)
      yield (adjplayer, adjboss, not isPlayerTurn), 0

def isDone(node: Node) -> bool:
  _, boss, _ = node
  return boss.hitpoints <= 0

def part1() -> None:
  player = Player(hitpoints=50, mana=500)
  boss = parseBoss()

  print('start:', player, boss)

  r = dijkstra((player, boss, True), getAdjacent, isDone)
  print('done:', r)
  print(r[1])

def part2() -> None:
  player = Player(hitpoints=50, mana=500)
  boss = parseBoss()

  print('start:', player, boss)

  r = dijkstra(
    (player, boss, True),
    lambda n: getAdjacent(n, hardMode=True),
    isDone,
  )
  print('done:', r)
  print(r[1])

part2()
