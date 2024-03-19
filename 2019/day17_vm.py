from common.sparsegrid import SparseGrid
from intcode import IntcodeVM

input = open('day17.txt').read().split(',')

Coords = tuple[int, int]

def initMemory() -> dict[int, int]:
  return dict(zip(range(len(input)), list(map(int, input))))

def initGrid() -> SparseGrid:
  outputs = IntcodeVM.initFromInput(input).runAll()
  print('outputs', len(outputs))

  grid = SparseGrid(2)
  x, y = 0, 0
  for c in outputs:
    if c == 10:
      x = 0
      y += 1
    else:
      grid.setValue((x, y), chr(c))
      x += 1
  return grid

def findStart(grid: SparseGrid) -> Coords:
  start = None
  for coords in grid.getAllCoords():
    if grid.getValue(coords) not in ['.', '#']:
      assert start is None, 'cannot be multiple start positions'
      start = coords
  assert start is not None, 'did not find start'
  assert len(start) == 2, 'bad coords'
  return start

def createPath(grid: SparseGrid) -> list[str | int]:
  start = findStart(grid)
  print('start:', start, grid.getValue(start))
  assert grid.getValue(start) == '^', 'assuming robot starts up for convention'

  x, y = start
  dx, dy = 1, 0
  distance = 0
  path: list[int | str] = ['R'] # Cheating by hardcoding first instruction.
  while True:
    nx, ny = x + dx, y + dy
    if grid.getValue((nx, ny)) != '#':
      path.append(distance)
      distance = 0
      # Need to turn 90 degrees.
      tdeltas = [(1, 0), (-1, 0)] if dx == 0 else [(0, 1), (0, -1)]
      for tdx, tdy in tdeltas:
        tx, ty = x + tdx, y + tdy
        if grid.getValue((tx, ty)) == '#':
          match tdx, tdy:
            case (1, 0): t = 'L' if dy == 1 else 'R'
            case (-1, 0): t = 'L' if dy == -1 else 'R'
            case (0, 1): t = 'L' if dx == -1 else 'R'
            case (0, -1): t = 'L' if dx == 1 else 'R'
            case _: assert False, 'bad turn deltas'

          dx, dy = tdx, tdy
          path.append(t)
      if path[-1] not in ['L', 'R']:
        # We needed to turn but couldn't. We must be at the end of the path.
        return path
    else:
      assert grid.getValue((nx, ny)) == '#', \
        'robot veered from scaffolding: (%d, %d): %s' % (nx, ny, path)
      distance += 1
      x, y = nx, ny

def funcToAscii(func: list) -> list[int]:
  result = []
  for e in func:
    # Multi-digit ints need to be broken up.
    for es in str(e):
      result.append(ord(es))
    result.append(ord(','))
  result = result[:-1] # remove the last comma
  result.append(ord('\n'))
  assert len(result) <= 20, 'ascii func too long'
  return result

def part1() -> None:
  grid = initGrid()
  grid.print2D()

  w, h = grid.getMaxCoords()
  print('w x h:', w, h)

  intersections = []
  for x, y in grid.getAllCoords():
    isIntersection = True
    for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
      if grid.getValue((x + dx, y + dy), '.') != '#':
        isIntersection = False
        break
    if isIntersection:
      intersections.append((x, y))

  print('intersections:', len(intersections))
  print(sum([x * y for x, y in intersections]))

def part2() -> None:
  grid = initGrid()
  grid.print2D()

  path = createPath(grid)
  print('path', len(path), path)

  # Determined by inspecting the path.
  funcs = {
    'A': ['R', 12, 'L', 8, 'R', 12],
    'B': ['R', 8, 'R', 6, 'R', 6, 'R', 8],
    'C': ['R', 8, 'L', 8, 'R', 8, 'R', 4, 'R', 4],
  }
  main = ['A', 'B', 'A', 'B', 'C', 'C', 'B', 'C', 'B', 'A']

  # Verify routines are correct.
  pi, mi = 0, 0
  while mi < len(main):
    func = funcs[main[mi]]
    for e in func:
      assert e == path[pi], 'func did not match path: %s' % str((mi, pi, main[mi], e))
      pi += 1
    mi += 1

  inputs = []
  inputs.extend(funcToAscii(main))
  inputs.extend(funcToAscii(funcs['A']))
  inputs.extend(funcToAscii(funcs['B']))
  inputs.extend(funcToAscii(funcs['C']))
  inputs.extend(funcToAscii(['n']))
  print('inputs', inputs)

  memory = initMemory()
  assert memory[0] == 1, 'bad value at address 0'
  memory[0] = 2 # wake up the robot
  outputs = IntcodeVM(memory).addInputs(inputs).runAll()
  print('outputs:', len(outputs))
  print(outputs[-1])

part2()
