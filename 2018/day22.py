from functools import cache
from enum import IntEnum
from typing import Iterable

from common.shortestpath import dijkstra

input = open('day22.txt').read().splitlines()

class TerrainType(IntEnum):
  ROCKY = 0
  WET = 1
  NARROW = 2

class Item(IntEnum): # needs to be IntEnum instead of Enum so dijkstra can break ties
  TORCH = 1
  CLIMBING = 2
  NEITHER = 3

Coords = tuple[int, int]
Node = tuple[Coords, Item]

def geologicIndex(x: int, y: int, tx: int, ty: int, depth: int) -> int:
  assert x >= 0 and y >= 0

  if x == 0 and y == 0:
    return 0

  if x == tx and y == ty:
    return 0

  if x == 0:
    return y * 48271

  if y == 0:
    return x * 16807

  m = 20183
  return (erosionLevel(x - 1, y, tx, ty, depth) * erosionLevel(x, y - 1, tx, ty, depth)) % m

@cache
def erosionLevel(x: int, y: int, tx: int, ty: int, depth: int) -> int:
  m = 20183
  geo = geologicIndex(x, y, tx, ty, depth)
  return (geo + depth) % m

def part1() -> None:
  depth = int(input[0].split(': ')[1])
  tx, ty = map(int, input[1].split(': ')[1].split(','))

  print('depth/target:', depth, tx, ty)

  ans = 0
  for x in range(tx + 1):
    for y in range(ty + 1):
      ans += erosionLevel(x, y, tx, ty, depth) % 3
  print(ans)

def part2() -> None:
  depth = int(input[0].split(': ')[1])
  tx, ty = map(int, input[1].split(': ')[1].split(','))

  print('depth/target:', depth, tx, ty)

  # Precompute erosion levels, because computing them with an empty @cache
  # will cause a stack overflow.
  for x in range(100 * tx + 1):
    for y in range(ty + 1):
      erosionLevel(x, y, tx, ty, depth)
  print('done precompute. running dijkstra...')

  def t(x: int, y: int) -> TerrainType:
    return TerrainType(erosionLevel(x, y, tx, ty, depth) % 3)

  def getAdj(n: Node) -> Iterable[tuple[Node, int]]:
    (x, y), item = n
    deltas = [(-1, 0),(1, 0),(0,-1),(0,1)]
    options = {
      TerrainType.ROCKY: {Item.TORCH, Item.CLIMBING},
      TerrainType.WET: {Item.NEITHER, Item.CLIMBING},
      TerrainType.NARROW: {Item.TORCH, Item.NEITHER},
    }

    # Generate states for switching to each item.
    for it in Item:
      if it == item:
        # We already have this item equipped. No-op.
        continue

      if it not in options[t(x, y)]:
        # The item not valid for current region. Skip.
        continue

      # Switching an item takes seven minutes.
      yield ((x, y), it), 7

    # Generate states for moving.
    for dx, dy in deltas:
      nx, ny = x + dx, y + dy
      if nx < 0 or ny < 0:
        # Invalid location.
        continue

      if item in options[t(nx, ny)]:
        # We're eqipped to move to this region, which takes one minute.
        yield ((nx, ny), item), 1

  def isDone(n: Node) -> bool:
    (x, y), item = n
    # We're done when we reach the target and have the torch equipped.
    return x == tx and y == ty and item == Item.TORCH

  start = ((0, 0), Item.TORCH)
  r = dijkstra(start, getAdj, isDone)
  print('result:', r)
  print(r[1])

part2()
