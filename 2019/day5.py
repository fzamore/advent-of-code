input = open('day5.txt').read().split(',')

def getParameterValues(memory: list[int], baseI: int) -> list[int]:
  value = memory[baseI]
  opcode = value % 100
  paramModes = str(value // 100)
  if opcode in [1, 2, 5, 6, 7, 8]: # all two-value-param opcodes
    if len(paramModes) == 1:
      paramModes = '0' + paramModes
    assert len(paramModes) == 2

  values = []
  for i in range(len(paramModes)):
    mode = paramModes[len(paramModes) - i - 1]
    match mode:
      case '0':
        address = memory[baseI + i + 1]
        value = memory[address]
      case '1':
        value = memory[baseI + i + 1]
      case _:
        assert False, 'bad mode: %s' % mode
    values.append(value)
  assert len(values) in [1, 2], 'bad values: %s' % values
  return values

def runMachine(memory: list[int], input: int) -> None:
  i = 0
  while (value := memory[i]) != 99:
    opcode = value % 100
    paramValues = getParameterValues(memory, i)
    match opcode:
      case 1:
        assert len(paramValues) == 2, 'bad addition: %s' % [i, value, paramValues]
        dst = memory[i + 3]
        memory[dst] = paramValues[0] + paramValues[1]
        i += 4
      case 2:
        assert len(paramValues) == 2, 'bad multiplication: %s' % [i, value, paramValues]
        dst = memory[i + 3]
        memory[dst] = paramValues[0] * paramValues[1]
        i += 4
      case 3:
        dst = memory[i + 1]
        print('input inst at:', i)
        memory[dst] = input
        i += 2
      case 4:
        assert len(paramValues) == 1, 'bad output: %s' % paramValues
        print('OUTPUT:', paramValues[0])
        i += 2
      case 5:
        assert len(paramValues) == 2, 'bad jump-if-true: %s' % [i, value, paramValues]
        if paramValues[0] != 0:
          i = paramValues[1]
        else:
          i += 3
      case 6:
        assert len(paramValues) == 2, 'bad jump-if-false: %s' % [i, value, paramValues]
        if paramValues[0] == 0:
          i = paramValues[1]
        else:
          i += 3
      case 7:
        assert len(paramValues) == 2, 'bad less than: %s' % [i, value, paramValues]
        dst = memory[i + 3]
        memory[dst] = 1 if paramValues[0] < paramValues[1] else 0
        i += 4
      case 8:
        assert len(paramValues) == 2, 'bad equals: %s' % [i, value, paramValues]
        dst = memory[i + 3]
        memory[dst] = 1 if paramValues[0] == paramValues[1] else 0
        i += 4
      case _:
        assert False, 'bad opcode: %s' % opcode

def part1() -> None:
  memory = list(map(int, input))
  runMachine(memory, 1)

def part2() -> None:
  memory = list(map(int, input))
  runMachine(memory, 5)

part2()
