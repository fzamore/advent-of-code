from typing import Optional
from common.ints import ints
from common.arraygrid import ArrayGrid
from math import prod

input = open('day14.txt').read().splitlines()

Robot = tuple[int, int, int, int] # x, y, vx, vy
Coords = tuple[int, int]

def parseInput() -> list[Robot]:
  r = []
  for line in input:
    x, y, vx, vy = ints(line)
    r.append((x, y, vx, vy))
  return r

def iterateRobot(robot: Robot, width: int, height: int) -> Robot:
  x, y, vx, vy = robot
  x = (x + vx) % width
  y = (y + vy) % height
  return x, y, vx, vy

def iterateRobots(robots: list[Robot], width: int, height: int) -> list[Robot]:
  return [iterateRobot(r, width, height) for r in robots]

def printRobots(robots: list[Robot], width: int, height: int, treetop: Optional[Coords] = None) -> None:
  grid = ArrayGrid(width, height)
  for r in robots:
    x, y, _, _ = r
    v = grid.getValue(x, y, 0)
    grid.setValue(x, y, v + 1)

  if treetop is not None:
    tx, ty = treetop
    grid.setValue(tx, ty, '*')
  grid.print2D({None: '.'})

# This looks for a "right triangle" pattern such that the given robot is
# on top. The legs of the triangle are horizontal and vertical, the right
# angle of the triangle is in the lower-left, and thus the hypotenuse is
# at a 45 degree angle going NW / SE. This was originally meant to
# approximate the right side of a Christmas tree, but it ended up finding
# the correct pattern anyway.
def isTreeTopAtRobot(robot: Robot, robotSet: set[Coords]) -> bool:
  x, y, _, _ = robot
  treeHeight = 10
  for i in range(treeHeight):
    for j in range(i + 1):
      if (x + j, y + i) not in robotSet:
        return False
  return True

def part1() -> None:
  robots = parseInput()
  print('robots:', len(robots))

  width = 101
  height = 103
  n = 100

  for i in range(n):
    robots = iterateRobots(robots, width, height)

  quadrants = [
    (0, 0, width // 2, height // 2),
    (width // 2 + 1, 0, width, height // 2),
    (0, height // 2 + 1, width // 2, height),
    (width // 2 + 1, height // 2 + 1, width, height),
  ]

  quadrantCounts = [0, 0, 0, 0]
  for r in robots:
    x, y, _, _ = r
    for i, (qx1, qy1, qx2, qy2) in enumerate(quadrants):
      if qx1 <= x < qx2 and qy1 <= y < qy2:
        quadrantCounts[i] += 1
  print(prod(quadrantCounts))

def part2() -> None:
  robots = parseInput()
  print('robots:', len(robots))

  width = 101
  height = 103

  # Through experimentation, I found that the robots will reset to their
  # original states after 10402 iterations. This didn't end up being
  # needed to solve the problem, but it was an upper bound on the
  # solution.

  i = 0
  while True:
    robots = iterateRobots(robots, width, height)
    i += 1

    robotSet = set([(r[0], r[1]) for r in robots])
    for r in robots:
      if isTreeTopAtRobot(r, robotSet):
        # We've found the answer.
        printRobots(robots, width, height, (r[0], r[1]))
        print('tree top:', r)
        print(i)
        return

    if i % 1000 == 0:
      print('iteration:', i)

part2()
