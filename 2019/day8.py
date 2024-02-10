from collections import defaultdict

input = list(map(int, list(open('day8.txt').read().strip())))

def valueForCoordinate(data: list[int], layerNum: int, x: int, y: int) -> int:
  w = 25
  h = 6

  base = w * h * layerNum
  return data[base + y * w + x]

def pixelForCoordinate(data: list[int], x: int, y: int) -> str:
  layerNum = 0
  while (value := valueForCoordinate(data, layerNum, x, y)) == 2:
    layerNum += 1
  assert value in [0, 1], 'bad value'
  return '#' if value == 1 else ' '

def part1() -> None:
  w = 25
  h = 6

  print('len:', len(input))

  layerSize = w * h
  layers: dict[int, dict] = {}

  for i, v in enumerate(input):
    layerNum = i // layerSize
    if layerNum not in layers:
      layers[layerNum] = defaultdict(int)
    layer = layers[layerNum]
    layer[v] += 1

  print('num layers:', len(layers))

  minLayer = min(layers.values(), key=lambda layer: layer[0])
  print('minLayer:', minLayer)

  print(minLayer[1] * minLayer[2])

def part2() -> None:
  w = 25
  h = 6

  print()
  for y in range(h):
    for x in range(w):
      print(pixelForCoordinate(input, x, y), end='')
    print()
  print()

part2()

