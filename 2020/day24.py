from common.io import readfile
from common.sparsegrid import SparseGrid

# tiles are represented via a SparseGrid. Each entry in the grid represents a black tile

def getDeltas():
  return {
    'nw': (-1, 1),
    'ne': (1, 1),
    'e': (2, 0),
    'se': (1, -1),
    'sw': (-1, -1),
    'w': (-2, 0),
  }

def getDelta(s):
  return getDeltas()[s]
  
def flip(grid, tile):
  x, y = (0, 0)
  for s in tile:
    dx, dy = getDelta(s)
    x += dx
    y += dy
  print('flip', x, y, tile)
  c = (x, y)
  if grid.hasValue(c):
    grid.deleteValue(c)
  else:
    grid.setValue(c, 1)

def getAdjacentCoords(coords):
  deltas = getDeltas().values()
  x, y = coords
  for dx, dy in getDeltas().values():
    yield (x + dx, y + dy)
    
def countAdjacentBlackTiles(grid, coords):
  c = 0
  for nx, ny in getAdjacentCoords(coords):
    if grid.hasValue((nx, ny)):
      c += 1
  return c

def step(grid):
  newgrid = SparseGrid(2)
  whiteTilesToConsider = set()
  for coords in grid.getAllCoords():
    adjacentBlackTiles = countAdjacentBlackTiles(grid, coords)
    if adjacentBlackTiles > 0 and adjacentBlackTiles <= 2:
      # black tile stays black
      newgrid.setValue(coords, 1)
    
    # add all adjacent tiles to this black tile to the list of white tiles to consider
    whiteTilesToConsider |= set(getAdjacentCoords(coords))

  for coords in whiteTilesToConsider:
    if not grid.hasValue(coords) and countAdjacentBlackTiles(grid, coords) == 2:
      # white tile with exactly two adjacent black tiles. flip
      newgrid.setValue(coords, 1)
  
  return newgrid

def part1():
  tiles = []
  for line in readfile('day24.txt'):
    tile = []
    i = 0
    while i < len(line):
      c = line[i]
      if c in ['n', 's']:
        tile.append(line[i:i+2])
        i += 2
      elif c in ['e', 'w']:
        tile.append(c)
        i += 1
      else:
        assert False, 'bad line: %s' % line
    tiles.append(tile)

  print('tiles', len(tiles))

  grid = SparseGrid(2)
  for tile in tiles:
    flip(grid, tile)
  
  print(len(grid.getAllCoords()))

def part2():
  tiles = []
  for line in readfile('day24.txt'):
    tile = []
    i = 0
    while i < len(line):
      c = line[i]
      if c in ['n', 's']:
        tile.append(line[i:i+2])
        i += 2
      elif c in ['e', 'w']:
        tile.append(c)
        i += 1
      else:
        assert False, 'bad line: %s' % line
    tiles.append(tile)

  print('tiles', len(tiles))

  grid = SparseGrid(2)
  for tile in tiles:
    flip(grid, tile)

  n = 100
  for i in range(0, n):
    print('day', i, len(grid.getAllCoords()))
    grid = step(grid)
  
  print(len(grid.getAllCoords()))

part2()
