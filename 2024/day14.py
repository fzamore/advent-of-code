from common.ints import ints
from common.arraygrid import ArrayGrid
from math import prod

input = open('day14.txt').read().splitlines()

Robot = tuple[int, int, int, int] # x, y, vx, vy

def parseInput() -> list[Robot]:
  r = []
  for line in input:
    x, y, vx, vy = ints(line)
    r.append((x, y, vx, vy))
  return r

def iterateRobot(robot: Robot, width: int, height: int, step: int) -> Robot:
  x, y, vx, vy = robot
  x = (x + vx * step) % width
  y = (y + vy * step) % height
  return x, y, vx, vy

def iterateRobots(robots: list[Robot], width: int, height: int, step: int = 1) -> list[Robot]:
  return [iterateRobot(r, width, height, step) for r in robots]

def printRobots(robots: list[Robot], width: int, height: int) -> None:
  grid = ArrayGrid(width, height)
  for r in robots:
    x, y, _, _ = r
    v = grid.getValue(x, y, 0)
    grid.setValue(x, y, v + 1)
  grid.print2D({None: '.'})

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

part1()
