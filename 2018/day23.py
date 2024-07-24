from collections import namedtuple

input = open('day23.txt').read().splitlines()

Bot = namedtuple('Bot', ['pos', 'radius'])

def parseLine(line: str) -> Bot:
  v = line.split(', ')
  pos = tuple(map(int, v[0].split('=')[1][1:-1].split(',')))
  radius = int(v[1].split('=')[1])
  return Bot(pos, radius)

def isInRange(bot: Bot, satellite: Bot) -> bool:
  x, y, z = bot.pos
  sx, sy, sz = satellite.pos

  return abs(x - sx) + abs(y - sy) + abs(z - sz) <= bot.radius

def part1() -> None:
  bots = [parseLine(x) for x in input]
  print('bots:', len(bots))

  maxbot = max(bots, key=lambda b: b.radius)
  print('maxbot:', maxbot)

  print(len([b for b in bots if isInRange(maxbot, b)]))

part1()
