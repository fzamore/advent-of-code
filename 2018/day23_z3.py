from collections import namedtuple
from z3 import Int, IntVal, If, Ints, sat, Optimize # type: ignore

input = open('day23.txt').read().splitlines()

Coords = tuple[int, int, int]
Bot = namedtuple('Bot', ['pos', 'radius'])

def parseLine(line: str) -> Bot:
  v = line.split(', ')
  pos = tuple(map(int, v[0].split('=')[1][1:-1].split(',')))
  radius = int(v[1].split('=')[1])
  return Bot(pos, radius)

def manhattanDist(c1: Coords, c2: Coords) -> int:
  (x1, y1, z1), (x2, y2, z2) = c1, c2
  return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

def isInRange(bot: Bot, satellite: Bot) -> bool:
  return manhattanDist(bot.pos, satellite.pos) <= bot.radius

def part1() -> None:
  bots = [parseLine(x) for x in input]
  print('bots:', len(bots))

  maxbot = max(bots, key=lambda b: b.radius)
  print('maxbot:', maxbot)

  print(len([b for b in bots if isInRange(maxbot, b)]))

def part2() -> None:
  bots = [parseLine(x) for x in input]
  print('bots:', len(bots))

  def absZ3(x: Int) -> Int:
    return If(x >= 0, x, -x)

  x, y, z = Ints('x y z')
  countExpr = IntVal(0)
  opt = Optimize()
  for bot in bots:
    xb, yb, zb = bot.pos
    countExpr += If(absZ3(x - xb) + absZ3(y - yb) + absZ3(z - zb) <= bot.radius, 1, 0)

  opt.maximize(countExpr)
  opt.minimize(absZ3(x) + absZ3(y) + absZ3(z))
  # We can alternatively create variables and minimize/maximize those variables.
  # d = Int('d')
  # opt.add(d == absZ3(x) + absZ3(y) + absZ3(z))
  # opt.minimize(d)

  assert opt.check() == sat, 'could not find solution'
  model = opt.model()
  coords = (model[x], model[y], model[z])
  print('coords:', coords)
  print(model.eval(absZ3(x) + absZ3(y) + absZ3(z)))

part2()
