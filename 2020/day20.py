from common.io import readfile
from common.sparsegrid import SparseGrid
import math

#
# Each tile edge is identified by 1, 2, 3, or 4.
# Each tile also has a polarity (1 or -1 depending on whether it's flipped)
# By default, the top edge of each tile is 1, and it has a polarity of 1.

def getAdjacentEdgePolarity(e1, e2):
  if (e1 <= 2 and e2 <= 2) or (e1 >= 3 and e2 >= 3):
    return -1
  else:
    return 1

def findAdjacentEdge(tileEdges, tileID1, tileID2):
  for e1 in tileEdges[tileID1]:
    for e2 in tileEdges[tileID2]:
      polarity = getAdjacentEdgePolarity(e1, e2)
      if tileEdges[tileID1][e1] == tileEdges[tileID2][e2]:
        return (e1, e2, polarity)
      elif tileEdges[tileID1][e1] == tileEdges[tileID2][e2][::-1]:
        return (e1, e2, -polarity)
  return None

def findAdjacentTiles(tileEdges, tileID):
  adjacent = {}
  for otherTileID in tileEdges:
    if otherTileID == tileID:
      continue
    adjEdge = findAdjacentEdge(tileEdges, tileID, otherTileID)
    if adjEdge != None:
      tileEdge, otherTileEdge, polarity = adjEdge
      print(tileID, otherTileID, tileEdge, otherTileEdge, polarity)
      adjacent[tileEdge] = (otherTileID, otherTileEdge, polarity)
  return adjacent

def findCornerTiles(tileEdges):
  corners = []
  for tileID in tileEdges:
    adjCount = len(findAdjacentTiles(tileEdges, tileID))
    if adjCount == 2:
      corners.append(tileID)
  assert len(corners) == 4, 'did not find four corners: %s' % str(corners)
  return corners

def computeAdjacencies(tileEdges):
  adjacencies = {}
  for tileID in tileEdges:
    adjacencies[tileID] = findAdjacentTiles(tileEdges, tileID)
  return adjacencies

def getOppositeEdge(edge):
  return {1: 3, 2: 4, 3: 1, 4: 2}[edge]
  
def getNextEdge(edge, direction):
  assert direction in [1, -1], 'invalid direction: %s' % direction
  edges = [1, 2, 3, 4]
  return edges[(((edge - 1) + direction) % 4)]
  
def computeTileGrid(adjacencies):
  # find an arbitrary corner tile and assign it to (0,0)
  cornerTileID = None
  for tileID in adjacencies:
    if len(adjacencies[tileID]) == 2:
      cornerTileID = tileID
      break

  sideLen = int(math.sqrt(len(adjacencies)))
  
  e1, e2 = list(adjacencies[cornerTileID].keys())
  rightEdge = e1 if ((e1 % 4) + 1) == e2 else e2
  topEdge = getNextEdge(rightEdge, -1)
  
  tileGrid = {(0, 0): (cornerTileID, topEdge, 1)}
  print((0, 0), cornerTileID)

  # first row
  for x in range(1, sideLen):
    prevTileID, prevTopEdge, prevPolarity = tileGrid[(x - 1, 0)]
    prevRightEdge = getNextEdge(prevTopEdge, prevPolarity)
    nextTileID, nextLeftEdge, nextPolarity = adjacencies[prevTileID][prevRightEdge]
    # compute polarity based on previous tile polarity and this tile's polarity
    polarity = prevPolarity * nextPolarity
    tileGrid[(x, 0)] = (
      nextTileID, 
      getNextEdge(nextLeftEdge, polarity), 
      polarity,
    )
    print((x, 0), nextTileID, polarity)

  # other rows
  for y in range(1, sideLen):
    for x in range(0, sideLen):
      prevTileID, prevTopEdge, prevPolarity = tileGrid[(x, y - 1)]
      prevBottomEdge = getOppositeEdge(prevTopEdge)
      nextTileID, nextTopEdge, nextPolarity = adjacencies[prevTileID][prevBottomEdge]
      # compute polarity based on previous tile polarity and this tile's polarity 
      # relative to the previous tile's polarity
      polarity = prevPolarity * nextPolarity
      tileGrid[(x, y)] = (nextTileID, nextTopEdge, polarity)
      print((x, y), nextTileID, polarity)

  return tileGrid

# translates a given (x, y) coordinate, by rotating it so that the top edge 
# is identified by topEdge and so that it matches the given polarity. 
# gridSize is the side lenth of a square grid
def translateCoords(coords, topEdge, polarity, gridSize):
  x, y = coords
  if polarity == 1:
    match topEdge:
      case 1:
        return (x, y)
      case 2:
        return (y, gridSize - x - 1)
      case 3:
        return (gridSize - x - 1, gridSize - y - 1)
      case 4:
        return (gridSize - y - 1, x)
      case _:
        assert False, 'bad edge'
  else:
    match topEdge:
      case 1:
        return (gridSize - x - 1, y)
      case 2:
        return (gridSize - y - 1, gridSize - x - 1)
      case 3:
        return (x, gridSize - y - 1)
      case 4:
        return (y, x)

def computeCellGrid(tileGrid, tiles):
  grid = SparseGrid(2)
  sideLen = int(math.sqrt(len(tileGrid)))
  
  for tx in range(0, sideLen):
    for ty in range(0, sideLen):
      tileID, topEdge, polarity = tileGrid[(tx, ty)]
      for xi in range(1, 9):
        for yi in range(1, 9):
          if not tiles[tileID].hasValue((xi, yi)):
            continue
          # translated coords for individual grid
          tgx, tgy = translateCoords((xi, yi), topEdge, polarity, 10)

          # cell coords in overall grid (8 because we're chopping off borders)
          cx = 8 * tx + tgx
          cy = 8 * ty + tgy

          # subtract one to align with (0, 0) (taking into account stripping the
          # top and left borders)
          cx -= 1
          cy -= 1

          grid.setValue((cx, cy), '#')
          #grid.setValue((cy, cx), '#')

  return grid

def getMonsterGrid():
  # sea monster pattern:
  #                      # 
  #    #    ##    ##    ###
  #     #  #  #  #  #  #  
  #
  coords = [
    (18, 0),
    (0, 1),
    (5, 1),
    (6, 1),
    (11, 1),
    (12, 1),
    (17, 1),
    (18, 1),
    (19, 1),
    (1, 2),
    (4, 2),
    (7, 2),
    (10, 2),
    (13, 2),
    (16, 2),
  ]
  monsterGrid = SparseGrid(2)
  for coord in coords:
    monsterGrid.setValue(coord, '#')
  return monsterGrid

def hasMonster(grid, monsterGrid, coords, topEdge, polarity):
  monsterGridSize = \
    monsterGrid.getMaxCoords()[0] - monsterGrid.getMinCoords()[0] + 1
  
  sx, sy = coords
  for monsterCoords in monsterGrid.getAllCoords():
    # orient the monster grid appropriately and check the main grid
    mx, my = translateCoords(monsterCoords, topEdge, polarity, monsterGridSize)
    if not grid.hasValue((sx + mx, sy + my)):
      return False
  return True

def countMonsters(grid, monsterGrid, topEdge, polarity):
  count = 0
  minCoords = grid.getMinCoords()
  maxCoords = grid.getMaxCoords()

  for x in range(minCoords[0], maxCoords[0] + 1):
    for y in range(minCoords[1], maxCoords[1] + 1):
      #tx, ty = translateCoords((x, y), topEdge, polarity, gridSize)
      if hasMonster(grid, monsterGrid, (x, y), topEdge, polarity):
        print('found monster', x, y)
        count += 1
  return count

def part1():
  tileEdges = {}
  tileID = None
  lines = readfile('day20.txt')
  i = 0
  while i < len(lines):
    line = lines[i]
    if line == "":
      i += 1
      continue
    if line[0:4] == 'Tile':
      tileID = int(line.split()[1][:-1])
      i += 1
      continue
    
    assert tileID != None, 'missing tileID'
    assert len(line) == 10, 'bad line length: %s' % line
    # edge 1 is initially the top edge
    tile = {
      1: [c for c in line],
      2: [lines[j][9] for j in range(i, i + 10)],
      3: [c for c in lines[i + 9]],
      4: [lines[j][0] for j in range(i, i + 10)],
    }
    
    tileEdges[tileID] = tile
    i += 10

  print('tile count', len(tileEdges))

  corners = findCornerTiles(tileEdges)
  print(corners)
  print(math.prod(corners))

def part2():
  tileEdges = {}
  tiles = {}
  tileID = None
  lines = readfile('day20.txt')
  i = 0
  while i < len(lines):
    line = lines[i]
    if line == "":
      i += 1
      continue
    if line[0:4] == 'Tile':
      tileID = int(line.split()[1][:-1])
      i += 1
      continue
    
    assert tileID != None, 'missing tileID'
    assert len(line) == 10, 'bad line length: %s' % line
    tileEdge = {
      1: [c for c in line],
      2: [lines[j][9] for j in range(i, i + 10)],
      3: [c for c in lines[i + 9]], 
      4: [lines[j][0] for j in range(i, i + 10)],
    }

    tile = SparseGrid(2)
    for x in range(0, 10):
      for y in range(0, 10):
        c = lines[i + y][x]
        if c == '#':
          tile.setValue((x, y), '#')
    tiles[tileID] = tile
    
    tileEdges[tileID] = tileEdge
    i += 10

  print('tile count', len(tileEdges))
  
  adjacencies = computeAdjacencies(tileEdges)
  print()

  tileGrid = computeTileGrid(adjacencies)
  #print(tileGrid)
  print()

  grid = computeCellGrid(tileGrid, tiles)
  grid.print2D(default='.')
  print()

  monsterGrid = getMonsterGrid()
  print('monster pattern:')
  monsterGrid.print2D(default=' ')

  gridValuesCount = len(grid.getAllCoords())
  monsterSize = len(monsterGrid.getAllCoords())
  for topEdge in [1, 2, 3, 4]:
    for polarity in [1, -1]:
      c = countMonsters(grid, monsterGrid, topEdge, polarity)
      if c > 0:
        print('countMonsters', topEdge, polarity, c, gridValuesCount - c * monsterSize)
      
part2()
