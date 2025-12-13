from typing import Generator, Iterable
from sympy import Matrix, zeros # type: ignore[import]
from common.ints import ints
from common.shortestpath import dijkstra

data = open('day10.txt').read().splitlines()

Lights = tuple[bool, ...]
Button = list[int]
Joltages = tuple[int, ...]

def parse() -> list[tuple[Lights, list[Button], Joltages]]:
  r = []
  for line in data:
    assert line.count(']') == 1, 'bad input line'
    target = tuple(c == '#' for c in line[1:line.index(']')])

    v = line.split()
    assert len(v) >= 3, 'bad input line'
    buttons = [ints(e) for e in v[1:-1]]

    assert line.count('{') == 1, 'bad input line'
    joltages = tuple(ints(line[line.index('{'):]))

    r.append((target, buttons, joltages))

  return r

def toggleLights(state: Lights, button: Button) -> Lights:
  return tuple(not state[i] if i in button else state[i] for i in range(len(state)))

def solveForLights(target: Lights, buttons: list[Button]) -> int:
  n = len(target)
  start = tuple(False for _ in range(n))

  def getAdj(state: Lights) -> Iterable[tuple[Lights, int]]:
    for button in buttons:
      yield toggleLights(state, button), 1

  def isDone(state: Lights) -> bool:
    return state == target

  r = dijkstra(start, getAdj, isDone)
  return int(r[1])

# Augmented matrix is a matrix such that each row is a linear equation,
# and each column (except the last column) contains variable coefficients.
# The last column contains constants that are alone on the right side of
# each equation.
def convertToAugmentedMatrix(buttons: list[Button], joltages: Joltages) -> Matrix:
  cols = len(buttons) + 1
  rows = len(joltages)
  m = zeros(rows, cols)

  for i, joltage in enumerate(joltages):
    m[i, -1] = joltage

  for i in range(rows):
    for j, button in enumerate(buttons):
      if i in button:
        m[i, j] = 1

  return m

def solveAugmentedMatrix(m: Matrix) -> int:
  print('matrix shape:', m.shape)
  print(f'{m=}')
  rows, cols = m.shape

  # Reduced Row Echelon Form (RREF) of a matrix is such that the leading
  # entry (that is, the leftmost non-zero entry) of every non-zero row
  # (called the pivot), is value 1 and is to the right of the leading
  # entry of every row above. There is only one RREF of any matrix.
  # Transforming a matrix to RREF essentially is equivalent to solving
  # each equation for one variable. Each leading entry in the matrix
  # represents a "basic" variable, and the rest of the variables are
  # called "free" variables. We test all possible combinations of free
  # variables (for this input there are at most three per line).
  #
  # https://en.wikipedia.org/wiki/Row_echelon_form#Reduced_row_echelon_form

  # This sympy function transforms to RREF (the only reason why I'm using sympy).
  rref, pivotColumns = m.rref()
  print(f'{rref=}')
  basicVars = pivotColumns
  freeVars = tuple([i for i in range(cols - 1) if i not in basicVars])
  print('vars:', basicVars, freeVars)

  # Find an upper bound for the free variables to reduce the search space.
  # Each free variable cannot be negative, and the sum of all free
  # variables cannot exceed this bound.
  lastCol = m.col(-1)
  bound = round(max(abs(v) for v in lastCol)) + 1
  print('bound:', bound)

  allTestValues: Generator[list[int], None, None]
  match len(freeVars):
    case 0:
      # This is a generator with a single entry. Make the typechecker happy.
      allTestValues = ([] for _ in range(1))
    case 1:
      allTestValues = ([x] for x in range(bound))
    case 2:
      allTestValues = ([x, y] for x in range(bound) for y in range(bound - x))
    case 3:
      allTestValues = ([x, y, z] for x in range(bound) for y in range(bound - x) for z in range(bound - x - y))
    case _:
      # The input is constructed to guarantee this.
      assert False, 'must have <= 3 free vars'

  lastRrefCol = rref.col(-1)
  best = None
  for testValues in allTestValues:
    total = sum(testValues)
    isValid = True
    for basicVar in basicVars:
      row = [i for i in range(rows) if rref[i, basicVar] != 0][0]
      varValue = lastRrefCol[row] - \
        sum(tv * rref[row, freeVars[tvi]] for (tvi, tv) in enumerate(testValues))
      if varValue < 0 or not varValue.is_integer:
        isValid = False
        break
      total += varValue

    if isValid:
      best = min(best, total) if best is not None else total

  assert best is not None, 'did not find answer'
  return best

def part1() -> None:
  parsed = parse()
  print('data:', len(parsed))
  ans = 0
  for target, buttons, _ in parsed:
    result = solveForLights(target, buttons)
    print('result:', result)
    ans += result
  print(ans)

def part2() -> None:
  parsed = parse()
  print('data:', len(parsed))

  print()
  print('*** PART 2 IS VERY SLOW: 2m using pypy and 4m using python ***')
  print()

  ans = 0
  for _, buttons, joltages in parsed:
    m = convertToAugmentedMatrix(buttons, joltages)
    result = solveAugmentedMatrix(m)
    print('result:', result)
    ans += result
    print("\n---\n")
  print(ans)

part2()
