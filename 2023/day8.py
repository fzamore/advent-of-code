input = open('day8.txt').read().splitlines()

def part1():
  instructions = input[0]
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


part1()
