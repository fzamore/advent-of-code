from typing import Callable
from common.arraygrid import ArrayGrid
from common.ints import ints

AdjustFn = Callable[[ArrayGrid, int, int], None]

data = open('day6.txt').read().splitlines()

def turnOn(grid: ArrayGrid, x: int, y: int) -> None:
  grid.setValue(x, y, 1)

def turnOff(grid: ArrayGrid, x: int, y: int) -> None:
  grid.setValue(x, y, 0)

def toggle(grid: ArrayGrid, x: int, y: int) -> None:
  v = grid.getValue(x, y, 0)
  grid.setValue(x, y, 1 if v == 0 else 0)

def adjust(grid: ArrayGrid, x: int, y: int, d: int) -> None:
  v = grid.getValue(x, y, 0)
  grid.setValue(x, y, max(0, v + d))

def execute(grid: ArrayGrid, turnOnFn: AdjustFn, turnOffFn: AdjustFn, toggleFn: AdjustFn) -> int:
  for i, line in enumerate(data):
    if i % 10 == 0:
      print('instr:', i)
    x1, y1, x2, y2 = ints(line)
    v = line.split()
    if v[0] == 'toggle':
      fn = toggleFn
    elif v[1] == 'on':
      fn = turnOnFn
    elif v[1] == 'off':
      fn = turnOffFn
    else:
      assert False, 'bad instr'

    for y in range(y1, y2 + 1):
      for x in range(x1, x2 + 1):
        fn(grid, x, y)

  return sum([v for (_, _, v) in grid.getItems(0)])

def part1() -> None:
  w, h = 1000, 1000
  grid = ArrayGrid(w, h)

  print('instrs:', len(data))

  ans = execute(grid, turnOn, turnOff, toggle)
  print(ans)

def part2() -> None:
  w, h = 1000, 1000
  grid = ArrayGrid(w, h)

  print('instrs:', len(data))

  def genAdj(d: int) -> AdjustFn:
    return lambda g, x, y: adjust(g, x, y, d)

  ans = execute(grid, genAdj(1), genAdj(-1), genAdj(2))
  print(ans)

part2()
