from collections import defaultdict

input = open('day20.txt').read().splitlines()

Coords = tuple[int, int, int]
Velocity = tuple[int, int, int]
Acceleration = tuple[int, int, int]
Particle = tuple[Coords, Velocity, Acceleration]

def parseTriple(s: str) -> tuple[int, int, int]:
  v0, v1, v2 = map(int, s[3:-1].split(','))
  return v0, v1, v2

def parseInput() -> list[Particle]:
  particles = []
  for line in input:
    p, v, a = line.split(', ')
    particles.append((
      parseTriple(p),
      parseTriple(v),
      parseTriple(a),
    ))
  return particles

def absTriple(t: tuple[int, int, int]) -> int:
  return abs(t[0]) + abs(t[1]) + abs(t[2])

def tickSingle(particle: Particle) -> Particle:
  p, v, a = particle
  x, y, z = p
  vx, vy, vz = v
  ax, ay, az = a
  vx, vy, vz = vx + ax, vy + ay, vz + az
  x, y, z = x + vx, y + vy, z + vz
  return (
    (x, y, z),
    (vx, vy, vz),
    a
  )

def tickAll(particles: list[Particle]) -> list[Particle]:
  positions = defaultdict(list)
  for particle in particles:
    nparticle = tickSingle(particle)
    positions[nparticle[0]].append(nparticle)
  # Remove collisions.
  return [positions[pos][0] for pos in positions if len(positions[pos]) == 1]

def part1() -> None:
  particles = parseInput()
  print('particles:', len(particles))
  # Find the particle with the minimum acceleration; break ties with minimum initial velocity.
  closest = min(
    particles,
    key=lambda p: (absTriple(p[2]), absTriple(p[1])),
  )
  print('closest:', closest)
  print(particles.index(closest))

def part2() -> None:
  particles = parseInput()
  print('particles:', len(particles))

  # By experimentation, after 500 ticks, all collisions will have been
  # resolved. This is a somewhat lame approach.
  n = 500
  for i in range(n):
    particles = tickAll(particles)
    if i % 100 == 0:
      print('particle count:', i, len(particles))
  print(len(particles))

part2()
