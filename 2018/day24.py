from dataclasses import dataclass
from copy import deepcopy
from typing import Optional

input = open('day24.txt').read().splitlines()

@dataclass
class Group:
  units: int
  hp: int
  damage: int
  attack: str
  initiative: int
  weaknesses: list[str]
  immunities: list[str]

  def effectivePower(self) -> int:
    return self.units * self.damage

Army = dict[int, Group] # An army is a dict of groups keyed by initiative.

def parseParens(parenStr: str) -> tuple[list[str], list[str]]:
  weaknesses: list[str] = []
  immunities: list[str] = []
  for g in parenStr.split('; '):
    v = g.split()
    assert len(v) >= 2
    match v[0]:
      case 'weak':
        l = weaknesses
      case 'immune':
        l = immunities
      case _:
        assert False, 'bad parenS: %s' % parenStr
    l.extend(''.join(v[2:]).split(','))
  return weaknesses, immunities

def parseLine(line: str) -> Group:
  weaknesses: list[str] = []
  immunities: list[str] = []
  if '(' in line:
    assert ')' in line
    start, end = line.find('(') + 1, line.find(')')
    weaknesses, immunities = parseParens(line[start:end])

  v = line.split()
  ints = []
  for val in v:
    if val.isnumeric():
      ints.append(int(val))
  assert len(ints) == 4, 'bad input line'

  return Group(
    ints[0],
    ints[1],
    ints[2],
    v[-5],
    ints[3],
    weaknesses,
    immunities,
  )

def parseInput() -> tuple[Army, Army]:
  immune: Army = {}
  infection: Army = {}

  army = None
  for line in input:
    if line == '':
      continue
    if line == 'Immune System:':
      army = immune
      continue
    if line == 'Infection:':
      army = infection
      continue

    assert army is not None, 'should have found army'
    group = parseLine(line)

    i = group.initiative
    assert i not in immune, 'already encountered initiative'
    assert i not in infection, 'already encountered initiative'
    army[i] = group

  return immune, infection

def computeDamage(attacker: Group, attackee: Group) -> int:
  eff = attacker.effectivePower()
  if attacker.attack in attackee.immunities:
    return 0
  if attacker.attack in attackee.weaknesses:
    return eff * 2
  return eff

def selectTarget(group: Group, enemyArmies: list[Group]) -> Optional[Group]:
  if group.units <= 0:
    return None

  if len(enemyArmies) == 0:
    return None

  # Sort by damage; break ties by effective power, then initiative.
  target = sorted(
    enemyArmies,
    reverse=True,
    key=lambda a: (computeDamage(group, a), a.effectivePower(), a.initiative),
  )[0]
  if computeDamage(group, target) == 0:
    # The "best" target would not incur any damage, so don't select a target.
    return None

  return target

# Select targets for all armies. Returns a list of (attacker, attackee) tuples.
def selectTargets(
  immuneArmy: Army,
  infectionArmy: Army,
) -> list[tuple[Group, Group]]:
  bothArmies = list(immuneArmy.values()) + list(infectionArmy.values())
  assert len(bothArmies) == len(immuneArmy) + len(infectionArmy), 'bad combining armies'

  # Make copies of the lists so we aren't deleting from the source data.
  immuneTargets = immuneArmy.copy()
  infectionTargets = infectionArmy.copy()

  targets = []

  # Sort by effective power; break ties by initiative.
  orderedGroups = sorted(
    bothArmies,
    reverse=True,
    key=lambda a: (a.effectivePower(), a.initiative),
  )
  for group in orderedGroups:
    if group.initiative in immuneArmy:
      enemyArmy = infectionTargets
    else:
      assert group.initiative in infectionArmy, 'army not in either group'
      enemyArmy = immuneTargets
    target = selectTarget(group, list(enemyArmy.values()))
    if target is not None:
      # Each target can only be targeted once.
      del enemyArmy[target.initiative]
      targets.append((group, target))

  return targets

def attackingPhase(targets: list[tuple[Group, Group]]) -> None:
  order = sorted(
    targets,
    reverse=True,
    key=lambda p: p[0].initiative,
  )
  for attacker, attackee in order:
    if attacker.units <= 0:
      continue
    damage = computeDamage(attacker, attackee)
    assert damage > 0, 'should not attack unless can inflict damage'

    kills = min(attackee.units, int(damage // attackee.hp))
    attackee.units -= kills
    assert attackee.units >= 0, 'units should never go below zero'

# Prunes an army by removing Groups with no units remaining.
def prune(army: Army) -> None:
  # Make a copy so we aren't modifying the list as we're iterating over it.
  for g in list(army.values()):
    if g.units == 0:
      del army[g.initiative]

def getTotalUnits(army: Army) -> int:
  return sum([g.units for g in army.values()])

def getWinner(immune: Army, infection: Army) -> Army:
  if len(immune) == 0:
    assert len(infection) > 0, 'infection should be winner'
    return infection
  else:
    assert len(infection) == 0 and len(immune) > 0, 'immune should be winner'
    return immune

# Returns whether the simulation is done.
def isDone(immune: Army, infection: Army) -> bool:
  return len(immune) == 0 or len(infection) == 0

# Executes the simulation and returns the winner, if any.
def execute(immune: Army, infection: Army) -> Optional[Army]:
  while not isDone(immune, infection):
    targets = selectTargets(immune, infection)

    totalUnits = getTotalUnits(immune) + getTotalUnits(infection)

    attackingPhase(targets)
    prune(immune)
    prune(infection)

    if totalUnits == getTotalUnits(immune) + getTotalUnits(infection):
      # Detect when no progress is being made. Otherwise, we will infinite loop in Part 2.
      return None

  return getWinner(immune, infection)

def boost(army: Army, amount: int) -> None:
  for k in army:
    army[k].damage += amount

def part1() -> None:
  immune, infection = parseInput()
  print('armies:', len(immune), len(infection))

  winner = execute(immune, infection)
  assert winner is not None, 'should\'ve found a winner'
  print(getTotalUnits(winner))

def part2() -> None:
  immuneOrig, infectionOrig = parseInput()
  print('armies:', len(immuneOrig), len(infectionOrig))

  # Who needs binary search when a linear scan is just fine.
  boostValue = 1
  while True:
    # We need to deepcopy to preserve the entire structure of each group.
    immune = deepcopy(immuneOrig)
    infection = deepcopy(infectionOrig)

    boost(immune, boostValue)
    winner = execute(immune, infection)
    print('end army sizes for boost:', boostValue, len(immune), len(infection))
    if winner is None:
      print('no winner for boost value:', boostValue)

    if winner == immune:
      print('immune is winner. end armies:', immune, infection)
      print(getTotalUnits(winner))
      return

    boostValue += 1

part2()
