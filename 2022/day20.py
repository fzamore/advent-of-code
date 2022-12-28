input = open('day20.txt').read().splitlines()

class Node:
  value: int
  next: 'Node'
  prev: 'Node'

  def __init__(self, value: int) -> None:
    self.value = value

# Returns the zero node and the ordered list.
def initNodelist(multiplier: int = 1) -> tuple[Node, list[Node]]:
  zero = None
  nodelist: list[Node] = []
  for line in input:
    v = int(line) * multiplier
    node = Node(v)
    if v == 0:
      assert zero is None
      zero = node
    nodelist.append(node)

  count = len(nodelist)
  for i in range(len(nodelist)):
    node = nodelist[i]
    prev = nodelist[(i - 1) % count]
    next = nodelist[(i + 1) % count]
    node.prev = prev
    node.next = next

  assert zero is not None
  return (zero, nodelist)

def verifyNodes(first: Node, count: int) -> None:
  c = 1
  p, n = first, first.next
  while n != first:
    assert n is not None
    assert n.prev is not None
    assert p == n.prev, 'bad prev pointer: %d, %d, %d' % (n.value, p.value, n.prev.value)
    assert n.prev == n.prev.prev.next
    assert n.next == n.next.next.prev
    p = n
    n = n.next
    c += 1
  assert c == count, 'bad count: %d, %d' % (c, count)

def printNodes(zero: Node) -> None:
  print()
  print('nodes: ', end='')
  print(zero.value, end='')
  n = zero.next
  while n != zero:
    assert n is not None
    print(', %d' % n.value, end='')
    n = n.next
  print()
  print()

def mix(nodelist: list[Node], count: int) -> None:
  for node in nodelist:
    v = node.value
    # We removed the current node from the list, so we have one fewer
    # spots in our modulus.
    toMove = v % (count - 1)
    if toMove == 0:
      # Nothing to move. Skip.
      continue

    prev = node.prev
    next = node.next
    # Remove node from this spot.
    node.next.prev = prev
    node.prev.next = next

    # Move forward. The mod operation above will convert negatives to
    # positives, so we only have to move right.
    assert toMove > 0
    for _ in range(toMove - 1):
      next = next.next
    assert node != next
    node.prev = next
    node.next = next.next
    node.next.prev = node
    node.prev.next = node

def listFromZeroNode(zero: Node) -> list[Node]:
  result = [zero]
  n = zero.next
  while n != zero:
    result.append(n)
    n = n.next
  return result

def part1():
  zero, nodelist = initNodelist()

  count = len(nodelist)
  print('count:', count)

  verifyNodes(zero, count)

  print('processing...')
  mix(nodelist, count)
  print('done')
  verifyNodes(zero, count)

  reordered = listFromZeroNode(zero)
  def getValue(i: int) -> int:
    return reordered[i % count].value

  v1, v2, v3 = getValue(1000), getValue(2000), getValue(3000)
  print(v1, v2, v3)
  print(v1 + v2 + v3)

def part2():
  key = 811589153
  zero, nodelist = initNodelist(key)

  count = len(nodelist)
  print('count:', count)

  verifyNodes(zero, count)

  print('processing...')
  for i in range(10):
    print('mixing round:', i + 1)
    mix(nodelist, count)
    verifyNodes(zero, count)
  print('done')

  reordered = listFromZeroNode(zero)
  verifyNodes(reordered[0], count)

  def getValue(i: int) -> int:
    return reordered[i % count].value

  v1, v2, v3 = getValue(1000), getValue(2000), getValue(3000)
  print(v1, v2, v3)
  print(v1 + v2 + v3)

part2()

