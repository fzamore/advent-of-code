from collections import namedtuple

input = list(map(int, open('day8.txt').read().split()))

Node = namedtuple('Node', ['start', 'children', 'metadata', 'size'])

def parseTree(i: int = 0) -> Node:
  numChildren = input[i]
  numMetadata = input[i + 1]

  if numChildren == 0:
    return Node(i, [], [input[i + 2 + x] for x in range(numMetadata)], numMetadata + 2)

  children = []
  offset = 2
  for _ in range(numChildren):
    child = parseTree(i + offset)
    offset += child.size
    children.append(child)

  metadata = []
  for _ in range(numMetadata):
    metadata.append(input[i + offset])
    offset += 1

  return Node(i, children, metadata, offset)

def value(node: Node) -> int:
  if len(node.children) == 0:
    return sum([m for m in node.metadata])

  s = 0
  for mi in node.metadata:
    if mi <= len(node.children):
      s += value(node.children[mi - 1])
  return s

def part1() -> None:
  print('input:', len(input))
  root = parseTree()
  assert root.size == len(input), 'bad root size'

  s = 0
  q = [root]
  while len(q) > 0:
    node = q.pop()
    s += sum([m for m in node.metadata])
    q.extend(node.children)
  print(s)

def part2() -> None:
  print('input:', len(input))
  root = parseTree()
  assert root.size == len(input), 'bad root size'
  print(value(root))

part2()
