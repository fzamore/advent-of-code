from collections import namedtuple
from common.sparsegrid import SparseGrid

input = open('day23.txt').read().splitlines()

Coords = tuple[int, int]

Rule = namedtuple('Rule', [
  'id', # N, E, S, or W
  'checks', # directions to check. always 3 (int, int) tuples
  'move', # direction to move. always 1 (int, int) tuple
])

def initGrid() -> SparseGrid:
  grid = SparseGrid(2)
  y = 0
  for line in input:
    x = 0
    for c in line:
      if c == '#':
        grid.setValue((x, y), c)
      x += 1
    y += 1
  return grid

def initRules() -> list[Rule]:
  return [
    Rule('N', [(0, -1), (-1, -1), (1, -1)], (0, -1)),
    Rule('S', [(0, 1), (-1, 1), (1, 1)], (0, 1)),
    Rule('W', [(-1, 0), (-1, -1), (-1, 1)], (-1, 0)),
    Rule('E', [(1, 0), (1, -1), (1, 1)], (1, 0)),
  ]

def shouldCheckElf(grid: SparseGrid, elf: Coords) -> bool:
  x, y = elf
  for dx in [-1, 0, 1]:
    for dy in [-1, 0, 1]:
      if dx == 0 and dy == 0:
        continue
      if grid.hasValue((x + dx, y + dy)):
        return True
  return False

def doRound(
  grid: SparseGrid,
  rules: list[Rule],
) -> list[Rule]:
  elves = grid.getAllCoords()

  # Generate proposals
  proposals: set[Coords] = set() # new location
  moves: dict[Coords, Coords] = {} # new location -> elf
  for x, y in elves:
    if not shouldCheckElf(grid, (x, y)):
      continue
    for rule in rules:
      applyRule = True
      for dx, dy in rule.checks:
        if grid.hasValue((x + dx, y + dy)):
          applyRule = False
          break
      if applyRule:
        rx, ry = rule.move
        assert rx == 0 or ry == 0, 'bad rule: (%d, %d)' % (rx, ry)
        move = (x + rx, y + ry)
        if move in proposals:
          del moves[move]
        else:
          moves[move] = (x, y)
        proposals.add(move)
        break

  # Make moves
  for move in moves:
    elf = moves[move]
    assert not grid.hasValue(move), \
      'cannot moved to occupied spot: (%d, %d)' % (move[0], move[1])
    grid.setValue(move, '#')
    grid.deleteValue(elf)

  # Shuffle rules
  return rules[1:] + [rules[0]]

def part1():
  grid = initGrid()

  rules = initRules()

  rounds = 10
  for _ in range(rounds):
    rules = doRound(grid, rules)

  xMin, yMin = 1, 1
  xMax, yMax = -1, -1
  allCoords = grid.getAllCoords()
  for x, y in allCoords:
    if x < xMin: xMin = x
    if x > xMax: xMax = x
    if y < yMin: yMin = y
    if y > yMax: yMax = y

  print(xMin, yMin, xMax, yMax)
  rectSize = (xMax - xMin + 1) * (yMax - yMin + 1)
  print(rectSize, len(allCoords))
  print(rectSize - len(allCoords))

part1()
