from dataclasses import dataclass
from typing import Optional

input = open('day20.txt').read().splitlines()

@dataclass
class Node:
  value: int
  index: int
  next: Optional['Node'] = None
  prev: Optional['Node'] = None

def verifyNodes(zero: Node, count: int) -> None:
  c = 1
  p, n = zero, zero.next
  while n != zero:
    assert n is not None
    assert n.prev is not None
    assert p == n.prev, 'bad prev pointer: %d, %d, %d' % (n.value, p.value, n.prev.value)
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

def part1():
  zero = None
  nodelist: list[Node] = []
  for i in range(len(input)):
    line = input[i]
    v = int(line)
    node = Node(v, i)
    if v == 0:
      assert zero is None
      zero = node
    nodelist.append(node)

  count = len(nodelist)
  print('count:', count)

  for i in range(len(nodelist)):
    node = nodelist[i]
    prev = nodelist[(i - 1) % count]
    next = nodelist[(i + 1) % count]
    node.prev = prev
    node.next = next

  verifyNodes(zero, count)

  print('processing...')
  for node in nodelist:
    v = node.value
    if v == 0:
      assert node == zero
      continue

    prev = node.prev
    next = node.next
    # Remove node from this spot.
    node.next.prev = prev
    node.prev.next = next

    if v > 0:
      for _ in range(v - 1):
        next = next.next
      assert node != next
      node.prev = next
      node.next = next.next
      node.next.prev = node
      node.prev.next = node
      verifyNodes(zero, count)

    if v < 0:
      for _ in range(abs(v) - 1):
        prev = prev.prev
      assert node != prev
      node.prev = prev.prev
      node.next = prev
      node.next.prev = node
      node.prev.next = node
      verifyNodes(zero, count)


  print('done')
  verifyNodes(zero, count)

  reordered = [zero]
  n = zero.next
  while n != zero:
    reordered.append(n)
    n = n.next

  def getValue(i: int) -> int:
    return reordered[i % count].value
  v1, v2, v3 = getValue(1000), getValue(2000), getValue(3000)
  print(v1, v2, v3)
  print(v1 + v2 + v3)

part1()

