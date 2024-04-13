from collections import defaultdict
from typing import Optional

input = open('day9.txt').read().split()

# Use a linked list.
class Node:
  value: int
  prev: 'Node'
  next: 'Node'

  def __init__(
    self,
    value: int,
    prev: Optional['Node'] = None,
    next: Optional['Node'] = None,
  ):
    self.value = value

    # Default to a self-loop if prev/next aren't specified.
    self.prev = prev if prev is not None else self
    self.next = next if next is not None else self

def solve(numPlayers: int, lastMarble: int) -> int:
  player = 0
  scores: dict[int, int] = defaultdict(int)

  cur = Node(0)

  for m in range(1, lastMarble + 1):
    if m % 23 == 0:
      toRemove = cur.prev.prev.prev.prev.prev.prev.prev
      scores[player] += m + toRemove.value

      toRemove.prev.next = toRemove.next
      toRemove.next.prev = toRemove.prev
      cur = toRemove.next

    else:
      prev = cur.next
      next = cur.next.next

      ncur = Node(m, prev, next)
      prev.next = ncur
      next.prev = ncur
      cur = ncur

    player = (player + 1) % numPlayers

  winner = max(scores, key=scores.__getitem__)
  print('winner (0-indexed):', winner)
  return scores[winner]

def part1() -> None:
  numPlayers = int(input[0])
  lastMarble = int(input[6])
  print('input:', numPlayers, lastMarble)

  print(solve(numPlayers, lastMarble))

def part2() -> None:
  numPlayers = int(input[0])
  lastMarble = int(input[6]) * 100
  print('input:', numPlayers, lastMarble)

  print(solve(numPlayers, lastMarble))

part2()
