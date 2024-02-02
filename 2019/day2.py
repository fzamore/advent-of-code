input = open('day2.txt').read().split(',')

def part1() -> None:
  values = list(map(int, input))

  values[1] = 12
  values[2] = 2

  i = 0
  while (opcode := values[i]) != 99:
    assert opcode in [1, 2], 'bad opcode: %s' % opcode
    i1, i2, dst = values[i + 1:i + 4]
    v1, v2 = values[i1], values[i2]
    print('inst:', opcode, i1, i2, dst)
    if opcode == 1:
      values[dst] = v1 + v2
    else:
      values[dst] = v1 * v2
    print('machine:', values)
    i += 4
  print(values[0])

part1()
