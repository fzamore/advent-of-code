input = open('day2.txt').read().split(',')

def runMachine(values: list[int]) -> None:
  i = 0
  while (opcode := values[i]) != 99:
    assert opcode in [1, 2], 'bad opcode: %s' % opcode
    i1, i2, dst = values[i + 1:i + 4]
    v1, v2 = values[i1], values[i2]
    if opcode == 1:
      values[dst] = v1 + v2
    else:
      values[dst] = v1 * v2
    i += 4

def part1() -> None:
  values = list(map(int, input))

  values[1] = 12
  values[2] = 2

  runMachine(values)
  print(values[0])

def part2() -> None:
  values = list(map(int, input))
  target = 19690720
  for i1 in range(0, 100):
    for i2 in range(0, 100):
      v = values.copy()
      v[1] = i1
      v[2] = i2
      runMachine(v)
      if v[0] == target:
        print('done:', i1, i2)
        print(100 * i1 + i2)
        return

  assert False, 'did not find solution'

part2()
