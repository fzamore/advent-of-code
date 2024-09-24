from collections import namedtuple

input = open('day13.txt').read().splitlines()

Layer = namedtuple('Layer', ['depth', 'range'])

def parseInput() -> list[Layer]:
  result = []
  for line in input:
    v = line.split(': ')
    result.append(Layer(int(v[0]), int(v[1])))
  return result

def isCaughtAtTime(layer: Layer, time: int) -> bool:
  # Treat each scanner as a repeating pattern of `m` steps.
  m = 2 * (layer.range - 1)
  assert m % 2 == 0, 'bad math'
  return time % m == 0

def execute(layers: list[Layer], delay: int = 0) -> list[Layer]:
  caught = []
  lastDepth = 0
  time = delay
  for layer in layers:
    time += (layer.depth - lastDepth)
    lastDepth = layer.depth
    if isCaughtAtTime(layer, time):
      caught.append(layer)
      if delay > 0:
        # HACK: If we're testing a nonzero delay, we're in Part 2 and thus
        # we don't care about all layers in which we're caught. We merely
        # care whether we're caught by *any* layer.
        return caught
  return caught

def part1() -> None:
  layers = parseInput()
  print('layers:', len(layers))
  caught = execute(layers)
  print(sum([layer.depth * layer.range for layer in caught]))

def part2() -> None:
  layers = parseInput()
  print('layers:', len(layers))

  delay = 1
  while len(execute(layers, delay)) > 0:
    delay += 1
  print(delay)

part2()
