from common.ints import ints
from math import prod

data = open('day6.txt').read().splitlines()

def part1() -> None:
  print('data:', len(data))
  h = len(data)
  w = len(data[0].split())
  operands = []
  operators = []
  for line in data:
    if '*' in line or '+' in line:
      operators = line.split()
      assert len(operators) == w, 'bad operators line'
    else:
      operands.append(ints(line))
      assert len(operands[-1]) == w, 'bad operands line'

  ans = 0
  for j in range(w):
    gen = (operands[i][j] for i in range(h - 1))
    match operators[j]:
      case '+':
        total = sum(gen)
      case '*':
        total = prod(gen)
      case _:
        assert False, 'bad operator'
    print('total:', j, total)
    ans += total
  print(ans)

def part2() -> None:
  print('data:', len(data))
  h = len(data)

  ranges = []
  start = 0
  for i in range(len(data[-1])):
    if data[-1][i] != ' ' and i != 0:
      ranges.append((start, i - 2))
      start = i
  ranges.append((start, len(data[-1]) - 1 ))

  ans = 0
  for start, end in ranges:
    operands = []
    for j in range(start, end + 1):
      s = (data[i][j] for i in range(h - 1) if data[i][j] != ' ')
      operands.append(int(''.join(s)))
    match data[-1][start]:
      case '+':
        total = sum(operands)
      case '*':
        total = prod(operands)
      case _:
        assert False, 'bad operator'
    print('total:', total)
    ans += total

  print(ans)

part2()
