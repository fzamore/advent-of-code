from collections import defaultdict, deque

input = open('day9.txt').read().split()

def solve(numPlayers: int, lastMarble: int) -> int:
  # I stole this approach from Reddit.
  #
  # Use a deque to represent the circle of marbles. Rotate the deque after
  # each operation to ensure the current marble is last. Rotation is
  # constant time in our case because the amount of rotation is small.
  circle = deque([0])
  scores: dict[int, int] = defaultdict(int)

  for m in range(1, lastMarble + 1):
    if m % 23 == 0:
      player = m % numPlayers
      circle.rotate(7)
      scores[player] += m + circle.pop()
      circle.rotate(-1)
    else:
      circle.rotate(-1)
      circle.append(m)

  winner = max(scores, key=scores.__getitem__)
  print('winner:', winner)
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
