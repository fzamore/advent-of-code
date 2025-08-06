from collections import namedtuple
from typing import Iterable
from common.ints import ints
from itertools import combinations

data = open('day21.txt').read().splitlines()

Character = namedtuple('Character', ['name', 'damage', 'armor', 'hitpoints'])

StoreItem = namedtuple('StoreItem', ['cost', 'damage', 'armor'])
StoreSection = dict[str, StoreItem]
Store = namedtuple('Store', ['weapons', 'armor', 'rings'])

def parseStore() -> Store:
  costs = '''
    Weapons:    Cost  Damage  Armor
    Dagger        8     4       0
    Shortsword   10     5       0
    Warhammer    25     6       0
    Longsword    40     7       0
    Greataxe     74     8       0

    Armor:      Cost  Damage  Armor
    Leather      13     0       1
    Chainmail    31     0       2
    Splintmail   53     0       3
    Bandedmail   75     0       4
    Platemail   102     0       5

    Rings:      Cost  Damage  Armor
    Damage +1    25     1       0
    Damage +2    50     2       0
    Damage +3   100     3       0
    Defense +1   20     0       1
    Defense +2   40     0       2
    Defense +3   80     0       3
  '''.splitlines()

  weapons: StoreSection = {}
  armor: StoreSection = {}
  rings: StoreSection = {}
  # Pretty janky parsing.
  for line in costs:
    v = ints(line)
    if len(v) == 0:
      continue
    if len(weapons) < 5:
      section = weapons
      itemname = line.split()[0]
      item = StoreItem(cost=v[0], damage=v[1], armor=v[2])
    elif len(armor) < 5:
      section = armor
      itemname = line.split()[0]
      item = StoreItem(cost=v[0], damage=v[1], armor=v[2])
    else:
      section = rings
      itemname = str(len(rings))
      item = StoreItem(cost=v[1], damage=v[2], armor=v[3])
    section[itemname] = item
  armor['No Armor'] = StoreItem(cost=0, damage=0, armor=0)
  return Store(weapons, armor, rings)

def ringCombos(store: Store) -> Iterable[StoreItem]:
  rings = store.rings
  yield StoreItem(cost=0, damage=0, armor=0)
  for ring in rings.values():
    yield ring
  for ring1, ring2 in combinations(rings.values(), 2):
    yield StoreItem(
      cost=ring1[0] + ring2[0],
      damage=ring1[1] + ring2[1],
      armor=ring1[2] + ring2[2],
    )

# Returns all possible purchases.
def getPossibleItemPurchases(store: Store):
  for weapon in store.weapons.values():
    for armor in store.armor.values():
      for ring in ringCombos(store):
        yield (
          weapon[0] + armor[0] + ring[0],
          weapon[1] + armor[1] + ring[1],
          weapon[2] + armor[2] + ring[2],
        )

def parseBoss() -> Character:
  # hitpoints, damage, armor
  d = []
  for line in data:
    v = ints(line)
    assert len(v) == 1, 'bad boss line'
    d.append(v[0])

  assert len(d) == 3, 'bad boss data'
  return Character('boss', damage=d[1], armor=d[2], hitpoints=d[0])

def attack(attacker: Character, attackee: Character) -> Character:
  damage = max(1, attacker.damage - attackee.armor)
  return attackee._replace(hitpoints=attackee.hitpoints - damage)

# Simulates the battle. Returns the name of the winner.
def fight(player: Character, boss: Character) -> str:
  while True:
    boss = attack(player, boss)

    if boss.hitpoints <= 0:
      return player.name

    player = attack(boss, player)
    if player.hitpoints <= 0:
      return boss.name

def canWinWithGold(store: Store, player: Character, boss: Character, gold: int, expectedWinner: str) -> bool:
  for purchase in getPossibleItemPurchases(store):
    cost, damage, armor = purchase
    if cost != gold:
      continue

    newplayer = player._replace(damage=player.damage + damage, armor=player.armor + armor)
    if fight(newplayer, boss) == expectedWinner:
      return True

  return False

def part1() -> None:
  store = parseStore()
  print('store:', store)

  player = Character('player', damage=0, armor=0, hitpoints=100)
  boss = parseBoss()
  print('boss:', boss)

  gold = 0
  while True:
    if canWinWithGold(store, player, boss, gold, player.name):
      print(gold)
      return
    gold += 1

def part2() -> None:
  store = parseStore()
  print('store:', store)

  player = Character('player', damage=0, armor=0, hitpoints=100)
  boss = parseBoss()
  print('boss:', boss)

  gold = 1000
  while True:
    if canWinWithGold(store, player, boss, gold, boss.name):
      print(gold)
      return
    gold -= 1

part2()
