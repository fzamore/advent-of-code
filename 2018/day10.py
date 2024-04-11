from common.sparsegrid import SparseGrid

input = open('day10.txt').read().splitlines()

Point = tuple[tuple[int, int], tuple[int, int]]

def parseLine(line: str) -> Point:
  # position=< 5, 11> velocity=< 1, -2>
  p = line.split('position=')[1].split('>')[0][1:].split(', ')
  v = line.split('velocity=')[1].split('>')[0][1:].split(', ')

  return (int(p[0]), int(p[1])), (int(v[0]), int(v[1]))

def step(points: list[Point]) -> list[Point]:
  npoints = []
  for pos, vel in points:
    x, y = pos
    vx, vy = vel

    x += vx
    y += vy
    npoints.append(((x, y), vel))

  return npoints

def hasMessage(points: list[Point]) -> bool:
  grid = makeGrid(points)

  # Check whether the points have a minimum number of vertical lines of a
  # minimum length.
  verticalLineLength = 7
  numVerticalLines = 3

  c = 0
  for x, y in grid.getAllCoords():
    i = 0
    while i < verticalLineLength and grid.hasValue((x, y + i)):
      i += 1
    if i == verticalLineLength:
      c += 1
      if c == numVerticalLines:
        return True
  return False

def makeGrid(points: list[Point]) -> SparseGrid:
  grid = SparseGrid(2)
  for (x, y), _ in points:
    grid.setValue((x, y), '#')
  return grid

def printPoints(points: list[Point]) -> None:
  grid = makeGrid(points)
  print()
  grid.print2D(default='.')

def part1() -> None:
  print('input:', len(input))
  points = []
  for line in input:
    pos, vel = parseLine(line)
    points.append((pos, vel))

  while not hasMessage(points):
    points = step(points)

  printPoints(points)

def part2() -> None:
  print('input:', len(input))
  points = []
  for line in input:
    pos, vel = parseLine(line)
    points.append((pos, vel))

  i = 0
  while not hasMessage(points):
    points = step(points)
    i += 1

  printPoints(points)
  print(i)

part2()
