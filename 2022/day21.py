from functools import cache


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

  @cache
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

part1()
