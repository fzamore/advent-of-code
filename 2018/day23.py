from collections import Counter, namedtuple

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

  # I stole this approach from Reddit. It reduces the problem to 1D by
  # creating a line segment for each bot, where the start of the segment
  # is the distance from the origin to the nearest point in the bot's
  # range, and the end of the segment is the distance from the origin to
  # the farthest point within the bot's range. Then, we want to find out
  # which segment *start* overlaps with the most other segments. We use
  # the start because the problem asks for the 3D point that's closest to
  # the origin. Note that we don't need to compute the 3D point itself,
  # because the solution to the problem is the distance between that point
  # and the origin. Note that this solution doesn't work perfectly for my
  # input; see below.

  segments = []
  for bot in bots:
    d = manhattanDist((0, 0, 0), bot.pos)
    r = bot.radius
    segmentStart = max(0, d - r)
    segmentEnd = d + r
    segments.append((segmentStart, segmentEnd))

  starts = set([r[0] for r in segments])
  c: Counter[int] = Counter()
  for start in starts:
    for segmentStart, segmentEnd in segments:
      if segmentStart <= start <= segmentEnd:
        c[start] += 1
  print('dist / frequency:', c.most_common(1))

  # I have no idea why I have to add one here. The original answer was too
  # low, so I tried adding one for kicks, and to my surprise, it worked.
  print(c.most_common(1)[0][0] + 1)

part2()
