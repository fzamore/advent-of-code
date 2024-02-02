from common.sparsegrid import SparseGrid

input = open('day3.txt').read().splitlines()

def getWirePoints(wire: list[str]) -> list[tuple[int, int]]:
  deltas = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, -1),
    'D': (0, 1),
  }

  px, py = (0, 0)
  results = []
  for inst in wire:
    dir = inst[0]
    qty = int(inst[1:])
    dx, dy = deltas[dir]
    for _ in range(qty):
      px = px + dx
      py = py + dy
      results.append((px, py))
  return results

def part1() -> None:
  wire1, wire2 = [x.split(',') for x in input]
  print('lengths:', len(wire1), len(wire2))

  wire1Points = getWirePoints(wire1)
  print('wire1Points:', len(wire1Points))

  wire2Points = getWirePoints(wire2)
  print('wire2Points:', len(wire2Points))

  ans = min([
    abs(x[0]) + abs(x[1]) for x in set(wire1Points).intersection(wire2Points)
  ])
  print(ans)


part1()
