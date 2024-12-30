from enum import Enum
from common.arraygrid import ArrayGrid, Delta

input = open('day2.txt').read().splitlines()

Coords = tuple[int, int]

class Dir(Enum):
  LEFT = 'L'
  RIGHT = 'R'
  UP = 'U'
  DOWN = 'D'

def initGrid1() -> tuple[ArrayGrid, Coords]:
  grid = ArrayGrid(3,3)
  for i in range(9):
    x = i % 3
    y = i // 3
    grid.setValue(x, y, str(i + 1))
  return grid, (1, 1)

def initGrid2() -> tuple[ArrayGrid, Coords]:
  data = [
    '..1..',
    '.234.',
    '56789',
    '.ABC.',
    '..D..',
  ]
  return ArrayGrid.gridFromInput(data), (0, 2)

def getDelta(dir: Dir) -> Delta:
  match dir:
    case Dir.LEFT: return -1, 0
    case Dir.RIGHT: return 1, 0
    case Dir.UP: return 0, -1
    case Dir.DOWN: return 0, 1

def advance(grid: ArrayGrid, pos: Coords, line: str) -> Coords:
  x, y = pos
  for c in line:
    dx, dy = getDelta(Dir(c))
    if grid.getValue(x + dx, y + dy, '.') != '.':
      x += dx
      y += dy
  return x, y

def getCode(grid: ArrayGrid, start: Coords) -> str:
  x, y = start
  code = []
  for line in input:
    x, y = advance(grid, (x, y), line)
    code.append(grid.getValue(x, y))
  return ''.join(code)

def part1() -> None:
  grid, start = initGrid1()
  grid.print2D()
  print(getCode(grid, start))

def part2() -> None:
  grid, start = initGrid2()
  grid.print2D()
  print(getCode(grid, start))

part2()
