from typing import Any

input = open('day21.txt').read().splitlines()

def parseInput() -> dict[str, str]:
  result = {}
  for line in input:
    v = line.split(': ')
    result[v[0]] = v[1]
  return result

def part1():
  data = parseInput()
  print(data)

  def resolve(key: str) -> int:
    value = data[key]
    if value.isdigit():
      return int(value)

    v = value.split()
    match v[1]:
      case '+': return resolve(v[0]) + resolve(v[2])
      case '-': return resolve(v[0]) - resolve(v[2])
      case '*': return resolve(v[0]) * resolve(v[2])
      case '/': return resolve(v[0]) // resolve(v[2])
      case _: assert False, 'bad data: %s, %s' % (key, value)

  print(resolve('root'))

def part2():
  data = parseInput()

  def resolve(key: str) -> int | tuple:
    assert key != 'root', 'cycle detected'
    if key == 'humn':
      return ('x',)
    value = data[key]
    if value.isdigit():
      return int(value)

    v = value.split()
    v1, v2 = resolve(v[0]), resolve(v[2])
    operator = v[1]
    bothInts = isinstance(v1, int) and isinstance(v2, int)
    if not bothInts:
      return (v1, v2, v[1])
    assert isinstance(v1, int)
    assert isinstance(v2, int)
    v1 = int(v1)
    v2 = int(v2)
    match operator:
      case '+': return v1 + v2
      case '-': return v1 - v2
      case '*': return v1 * v2
      case '/':
        assert v1 % v2 == 0
        return v1 // v2
      case _: assert False, 'bad data: %s, %s' % (key, value)

  def putInOrder(value: tuple) -> list[tuple]:
    if len(value) == 1:
      assert value[0] == 'x'
      return [('x',)]
    assert len(value) == 3
    operator = value[2]
    assert operator in ['+', '-', '*', '/'], 'bad operator'
    assert isinstance(value[0], int) or isinstance(value[1], int), 'bad operands'

    if isinstance(value[0], int):
      operand = int(value[0])
      rest = value[1]
      isOperandFirst = True
    else:
      operand = int(value[1])
      rest = value[0]
      isOperandFirst = False

    # mypy can be annoying sometimes
    result: list[tuple[Any, ...]] = [(operand, operator, isOperandFirst)]
    result.extend(putInOrder(rest))
    return result

  values = data['root'].split()
  print(data['root'], values)
  left = resolve(values[0])
  right = resolve(values[2])
  # The right side is always an int.
  assert isinstance(right, int), 'bad right value: %s' % str(right)
  print('left:')
  print(left)
  print('right:')
  print(right)
  print()

  inOrder = putInOrder(left)

  acc = right
  for value in inOrder:
    if len(value) == 1:
      assert value[0] == 'x'
      print(acc)
    else:
      assert len(value) == 3
      isOperandFirst = value[2]
      v = int(value[0])
      # Algebra!
      match value[1]:
        case '+':
          acc -= v
        case '-':
          if isOperandFirst:
            acc = v - acc
          else:
            acc += v
        case '*':
          assert acc % v == 0
          acc //= v
        case '/':
          if isOperandFirst:
            assert v % acc == 0
            acc = v // acc
          else:
            acc *= v

part2()
