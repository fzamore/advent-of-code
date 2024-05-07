from typing import Optional
from common.arraygrid import ArrayGrid
from dataclasses import dataclass
from common.graphtraversal import bfs

input = open('day15.txt').read().splitlines()

Coords = tuple[int, int]

@dataclass
class Unit:
  type: str
  pos: Coords
  hp: int
  power: int = 3

# This ensures positions are sorted in "reading" order.
def keyFunc(pos: Coords) -> tuple[int, int]:
  return pos[1], pos[0]

# Finds the unit which this unit should attack.
def getAttackee(grid: ArrayGrid, unit: Unit) -> Optional[Unit]:
  x, y = unit.pos
  candidates: list[Unit] = []
  for ax, ay in grid.getAdjacentCoords(x, y):
    av = grid.getValue(ax, ay)
    if isinstance(av, Unit) and av.type != unit.type:
      candidates.append(av)

  if len(candidates) == 0:
    return None

  return min(
    candidates,
    key=lambda u: (u.hp, u.pos[1], u.pos[0]),
  )

def attack(grid: ArrayGrid, attacker: Unit, attackee: Unit) -> None:
  attackee.hp -= attacker.power
  if attackee.hp <= 0:
    # The attackee has been killed.
    x, y = attackee.pos
    grid.setValue(x, y, '.')
    attackee.pos = (-1, -1)

# Returns the position of the closest adjacent enemy.
def getClosestAdjEnemyPos(grid: ArrayGrid, unit: Unit) -> Optional[Coords]:
  candidates: list[Coords] = []
  minSteps = 10000 # arbitrary
  def getAdj(node):
    x, y = node
    return [(p, None) for p in grid.getAdjacentCoords(x, y)]

  def visit(node, numSteps, _):
    nonlocal minSteps
    if numSteps > minSteps:
      # We've already found a closer enemy. Do not consider this node.
      return False

    x, y = node
    v = grid.getValue(x, y)
    if v != '.':
      return False

    for ax, ay in grid.getAdjacentCoords(x, y):
      av = grid.getValue(ax, ay)
      if isinstance(av, Unit) and av.type != unit.type:
        candidates.append((x, y))
        minSteps = min(minSteps, numSteps)
    return True

  bfs(unit.pos, getAdj, visit)
  if len(candidates) == 0:
    return None
  return min(candidates, key=keyFunc)

# Returns the minimum number of steps from src to dst, taking walls into account.
def getMinSteps(grid: ArrayGrid, src: Coords, dst: Coords) -> Optional[int]:
  def getAdj(node):
    x, y = node
    if node == dst:
      return []
    return [(p, None) for p in grid.getAdjacentCoords(x, y)]

  def visit(node, *_):
    x, y = node
    v = grid.getValue(x, y)
    return v == '.' or node == dst

  result = bfs(src, getAdj, visit)
  return result.get(dst)

# Returns the immediate next step toward the given enemy.
def getStepTowardEnemy(grid: ArrayGrid, pos: Coords, enemyPos: Coords) -> Coords:
  candidates: list[tuple[Coords, int]] = []

  x, y = pos
  for ax, ay in grid.getAdjacentCoords(x, y):
    av = grid.getValue(ax, ay)
    if av != '.':
      continue
    t = getMinSteps(grid, (ax, ay), enemyPos)
    if t is not None:
      candidates.append(((ax, ay), t))

  return min(candidates, key=lambda e: (e[1], e[0][1], e[0][0]))[0]

# Moves a unit according to combat rules. Does nothing if no suitable enemy is found.
def moveUnit(grid: ArrayGrid, unit: Unit) -> None:
  closestEnemyPos = getClosestAdjEnemyPos(grid, unit)
  if closestEnemyPos is None:
    return

  step = getStepTowardEnemy(grid, unit.pos, closestEnemyPos)

  nx, ny = step
  ox, oy = unit.pos

  unit.pos = step
  grid.setValue(nx, ny, unit)
  grid.setValue(ox, oy, '.')

# Returns whether combat is done (i.e., whether there is only one unit type left).
def isDone(units: list[Unit]) -> bool:
  return len(set([u.type for u in units if u.hp > 0])) == 1

# Performs one iteration of battle. Returns whether the round fully completed.
def iterate(grid: ArrayGrid, units: list[Unit]) -> bool:
  # Ensure we process units in the correct order.
  units = sorted(units, key=lambda u: keyFunc(u.pos))

  for unit in units:
    if isDone(units):
      # This round didn't complete.
      return False

    if unit.hp <= 0:
      # This unit is dead.
      continue

    attackee = getAttackee(grid, unit)
    if attackee is None:
      moveUnit(grid, unit)
      attackee = getAttackee(grid, unit)

    if attackee is not None:
      attack(grid, unit, attackee)

  return True

def printGrid(grid: ArrayGrid) -> None:
  ngrid = grid.copy()
  for y in range(grid.getHeight()):
    for x in range(grid.getWidth()):
      v = grid.getValue(x, y)
      if isinstance(v, Unit):
        ngrid.setValue(x, y, v.type)
  ngrid.print2D()

def battle(elfAttackPower: int) -> tuple[int, list[Unit]]:
  grid = ArrayGrid.gridFromInput(input)

  units: list[Unit] = []

  w, h = grid.getWidth(), grid.getHeight()
  for y in range(h):
    for x in range(w):
      v = grid.getValue(x, y)
      if v in ['G', 'E']:
        power = elfAttackPower if v == 'E' else 3
        u = Unit(v, (x, y), 200, power)
        units.append(u)
        grid.setValue(x, y, u)

  print('units:', len(units))

  i = 0
  while True:
    finished = iterate(grid, units)
    if finished:
      # The round completed.
      i += 1
    if isDone(units):
      return i, units

def part1() -> None:
  rounds, units = battle(3)
  outcome = rounds * sum([u.hp for u in units if u.hp > 0])
  print('done', rounds)
  print(outcome)

def part2() -> None:
  grid = ArrayGrid.gridFromInput(input)
  grid.print2D()

  lo, hi = 4, 100 # obtained by experimentation
  successfulOutcomes = {}

  # Binary search.
  while lo < hi - 1:
    mid = (lo + hi) // 2
    print()
    print('battling with attack power:', mid)
    print('search range:', lo, hi)
    rounds, units = battle(mid)
    elfLosses = len([u for u in units if u.hp <= 0 and u.type == 'E'])
    print('done battle', rounds)
    print('elf losses:', elfLosses)
    if elfLosses == 0:
      successfulOutcomes[mid] = rounds * sum([u.hp for u in units if u.hp > 0])
      hi = mid
    else:
      lo = mid

  print()
  minAttackPower = min(successfulOutcomes.keys())
  print('done search. min attack power:', minAttackPower)
  print(successfulOutcomes[minAttackPower])

part2()
