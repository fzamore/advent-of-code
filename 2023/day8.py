from math import lcm

input = open('day8.txt').read().splitlines()

def createNetwork() -> dict[str, dict[str, str]]:
  network = {}
  for line in input[2:]:
    values = line.split()
    node = values[0]
    assert len(node) == 3, 'bad node: %s' % node
    left = values[2][1:4]
    assert len(left) == 3, 'bad left: %s' % left
    right = values[3][0:3]
    assert len(right) == 3, 'bad right: %s' % right
    network[node] = {
      'L': left,
      'R': right,
    }
  return network

def part1():
  instructions = input[0]
  network = createNetwork()
  print(len(instructions), len(network))
  print()

  start = 'AAA'
  finish = 'ZZZ'
  i = 0
  n = start
  while True:
    inst = instructions[i % len(instructions)]
    n = network[n][inst]
    if n == finish:
      break
    i += 1
  print(i + 1)

def part2():
  instructions = input[0]
  network = createNetwork()
  print(len(instructions), len(network))

  starts = [x for x in network if x[2] == 'A']
  ends = [x for x in network if x[2] == 'Z']
  assert len(starts) == len(ends), 'mismatched starts/ends: %d %d' % (
    len(starts), len(ends),
  )
  print(starts, ends)
  print(len(starts))
  print()

  # Through experimentation, I determined that each start node will always
  # end up at the same finish node. Given this, the problem becomes to
  # calculate the number of steps it will take each start node to reach
  # its finish node, and then take the least common multiple of all of
  # those step counts.

  pathLengths = []
  for start in starts:
    i = 0
    n = start
    while True:
      inst = instructions[i % len(instructions)]
      n = network[n][inst]
      if n[2] == 'Z':
        print('path:', start, n, i + 1)
        pathLengths.append(i + 1)
        break
      i += 1

  print()
  print(lcm(*pathLengths))

part2()
