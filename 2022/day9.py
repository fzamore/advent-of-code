input = open('day9.txt').read().splitlines()

Coords =  tuple[int, int]
Rope = list[Coords]
ROPE_LEN  = 10

def getDelta(dir: str) -> Coords:
  assert len(dir) == 1, 'invalid direction: %s' % dir
  return {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
  }[dir]

def getDist(c1: Coords, c2: Coords) -> int:
  return max(abs(c2[0] - c1[0]), abs(c2[1] -  c1[1]))

# silly that this isn't a built-in
def clamp(n: int, smallest: int, largest: int) -> int:
  return max(smallest, min(n, largest))

# Step the head of the rope by the given delta, which must be exactly one
# Manhattan unit. This will return the new head position and new tail
# position (or "next knot" position, in the case of a multi-knot rope).
def stepHead(hpos: Coords, tpos: Coords, delta: Coords) -> tuple[Coords, Coords]:
  nhpos = (hpos[0] + delta[0], hpos[1] + delta[1])
  ntpos = stepTail(nhpos, tpos)
  return (nhpos, ntpos)

# Steps any tail knot according to the given new head position.
def stepTail(nhpos: Coords, tpos: Coords) -> Coords:
  dist = getDist(nhpos, tpos)
  if dist <= 1:
    # The head hasn't moved far enough to drag the tail anywhere.
    return tpos

  assert dist == 2, 'invalid movement'
  # Move the tail toward the head such that the tail moves at most one
  # unit in each x-y direction.
  tdelta = (
    clamp(nhpos[0] - tpos[0], -1, 1),
    clamp(nhpos[1] - tpos[1], -1, 1),
  )
  return (tpos[0] + tdelta[0], tpos[1] + tdelta[1])

# Steps an entire rope by the given delta, which must be exactly one
# Manhattan unit.
def stepRope(rope: Rope, delta: Coords) -> Rope:
  nrope = rope.copy()
  # first, move the head and knot 1, by assuming knot 0 is the head and
  # knot 1 is the tail
  nrope[0], nrope[1] = stepHead(nrope[0], nrope[1], delta)

  # next, move knots 2-{n-1}
  for i in range(2, ROPE_LEN):
    nrope[i] = stepTail(nrope[i - 1], nrope[i])

  return nrope

def part1():
  hpos = (0, 0)
  tpos = (0, 0)
  allTpos = {tpos}
  for line in input:
    values = line.split()
    delta, qty = getDelta(values[0]), int(values[1])
    print(values)
    for _ in range(qty):
      hpos, tpos = stepHead(hpos, tpos, delta)
      allTpos.add(tpos)
    print(hpos, tpos)
  print(len(allTpos))

def part2():
  rope = [(0, 0)] * ROPE_LEN
  allTpos = {rope[-1]}
  for line in input:
    values = line.split()
    delta, qty = getDelta(values[0]), int(values[1])
    print(values)
    for _ in range(qty):
      rope = stepRope(rope, delta)
      allTpos.add(rope[-1])
    print(rope)
  print(len(allTpos))

part2()
