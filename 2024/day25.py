from itertools import product
from common.arraygrid import ArrayGrid

input = open('day25.txt').read().split("\n\n")

def countInColumn(grid: ArrayGrid, x: int) -> int:
  return sum(1 for y in range(1, grid.getHeight() - 1) if grid.getValue(x, y) == '#')

def doesKeyFitInLock(lock: ArrayGrid, key: ArrayGrid) -> bool:
  assert lock.getWidth() == key.getWidth(), 'bad lock / key'
  return all(countInColumn(lock, x) + countInColumn(key, x) <= 5 for x in range(lock.getWidth()))

def part1() -> None:
  locks, keys = [], []
  for chunk in input:
    grid = ArrayGrid.gridFromInput(chunk.splitlines())
    if grid.getValue(0, 0) == '#':
      locks.append(grid)
    else:
      keys.append(grid)

  print('locks:', len(locks))
  print('keys:', len(keys))

  ans = sum(1 for (lock, key) in product(locks, keys) if doesKeyFitInLock(lock, key))
  print(ans)

part1()
