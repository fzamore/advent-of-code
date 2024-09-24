from collections import namedtuple

input = open('day13.txt').read().splitlines()

Layer = namedtuple('Layer', ['depth', 'range'])

def parseInput() -> list[Layer]:
  result = []
  for line in input:
    v = line.split(': ')
    result.append(Layer(int(v[0]), int(v[1])))
  return result

def getScannerPos(layer: Layer, time: int) -> int:
  # Treat each scanner as a repeating pattern of `m` steps.
  m = 2 * (layer.range - 1)
  assert m % 2 == 0, 'bad math'

  adjustedTime = time % m
  if adjustedTime <= m // 2:
    # Scanner is going out.
    assert adjustedTime <= layer.range, 'bad range math in outgoing trip'
    return adjustedTime
  else:
    # Scanner is coming back.
    base = layer.range - 1
    adjustedTime -= m // 2
    result = base - adjustedTime
    assert result <= layer.range, 'bad range math in return trip'
    return result

def part1() -> None:
  layers = parseInput()
  print('layers:', len(layers))

  severity = 0
  time = 0
  for layer in layers:
    assert time <= layer.depth, 'layers not sorted by depth'
    time = layer.depth
    scannerPos = getScannerPos(layer, time)
    print('scanner pos:', time, scannerPos)
    if scannerPos == 0:
      severity += layer.depth * layer.range

  print(severity)

part1()
