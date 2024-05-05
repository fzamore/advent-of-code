from dataclasses import dataclass
from typing import Optional
from common.sparsegrid import SparseGrid

input = open('day13.txt').read().splitlines()
# Pad the last line with spaces so the grid is a rectangle
input[-1] += ' ' * (len(input[0]) - len(input[-1]))

Coords = tuple[int, int]
@dataclass
class Cart:
  pos: Coords
  dir: str
  turn: int

def parseInput() -> tuple[SparseGrid, dict[int, Cart]]:
  grid = SparseGrid.gridFrom2DInput(input)

  cartid = 1
  carts = {}
  for c in grid.getAllCoords():
    v = grid.getValue(c)
    if v in ['<', '>', 'v', '^']:
      carts[cartid] = Cart((c[0], c[1]), v, 0)
      cartid += 1
      if v in ['<', '>']:
        grid.setValue(c, '-')
      else:
        grid.setValue(c, '|')
  return grid, carts

def makeTurn(dir: str, turn: int) -> str:
  turns = ['L', 'S', 'R']

  dirs = {
    'L': {
      '^': '<',
      '<': 'v',
      'v': '>',
      '>': '^',
    },
    'S': {
      '^': '^',
      '<': '<',
      'v': 'v',
      '>': '>',
    },
    'R': {
      '^': '>',
      '<': '^',
      'v': '<',
      '>': 'v',
    },
  }

  return dirs[turns[turn]][dir]

def getDir(gridValue: str, dir: str, turn: int):
  if gridValue in ['-', '|']:
    return dir

  match gridValue:
    case '+':
      return makeTurn(dir, turn)
    case '\\':
      match dir:
        case '^': return '<'
        case '<': return '^'
        case 'v': return '>'
        case '>': return 'v'
        case _: assert False
    case '/':
      match dir:
        case '^': return '>'
        case '<': return 'v'
        case 'v': return '<'
        case '>': return '^'
        case _: assert False
    case _:
      assert False, 'bad dir'

# Assume the input is constructed that there will be at most one collision per tick.
def getCollisionID(cart: Cart, cartid: int, carts: dict[int, Cart]) -> Optional[int]:
  for id in carts:
    if cartid == id:
      continue

    if cart.pos == carts[id].pos:
      print('collision', cart.pos)
      return id

  return None

# Executes one tick of the system by updating carts in-place. If
# `removeCollisions` is false, it stops immediately after the firts
# collisison and returns the location of that collision. Otherwise, all
# colliding carts are removed from the input.
def tick(
  grid: SparseGrid,
  carts: dict[int, Cart],
  *,
  removeCollisions = False,
) -> Optional[Coords]:

  deltas = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, -1),
    'v': (0, 1),
  }

  cartids = list(carts.keys())
  for cartid in cartids:
    cart = carts.get(cartid)
    if cart is None:
      # This cart may have already collided and been removed from the list.
      continue

    x, y = cart.pos
    dx, dy = deltas[cart.dir]
    nx, ny = x + dx, y + dy

    nv = grid.getValue((nx, ny))
    ndir = getDir(nv, cart.dir, cart.turn)
    nturn = cart.turn
    if nv == '+':
      nturn = (nturn + 1) % 3

    cart.pos = (nx, ny)
    cart.dir = ndir
    cart.turn = nturn

    collisionID = getCollisionID(cart, cartid, carts)
    if collisionID is None:
      # No collision. Keep going.
      continue

    if not removeCollisions:
      # We've found our collision. Stop.
      return carts[collisionID].pos

    # Remove both colliding carts.
    del carts[cartid]
    del carts[collisionID]

  return None

def part1() -> None:
  print()
  grid, carts = parseInput()
  print('carts', len(carts))
  print(carts)

  while (ans := tick(grid, carts)) is None:
    pass

  print('%d,%d' % (ans[0], ans[1]))

def part2():
  print()

  print()
  grid, carts = parseInput()
  print('carts', len(carts))
  print(carts)

  while len(carts) > 1:
    tick(grid, carts, removeCollisions=True)

  ans = carts[list(carts.keys())[0]].pos
  print('%d,%d' % (ans[0], ans[1]))

part2()
