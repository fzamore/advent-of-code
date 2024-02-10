from collections import defaultdict


input = list(map(int, list(open('day8.txt').read().strip())))

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

part1()

