from collections import defaultdict

input = open('day9.txt').read().split()

def place(placed: list[int], curI: int, marble: int) -> tuple[int, list[int]]:
  n = len(placed)
  if curI == n - 1:
    nCurI = 1
  else:
    nCurI = curI + 2
  return nCurI, placed[:nCurI] + [marble] + placed[nCurI:]

# This is slow (~15s).
def part1() -> None:
  players = int(input[0])
  lastMarble = int(input[6])

  placed = [0]
  curI = 0
  player = 0
  scores: dict[int, int] = defaultdict(int)

  print('input:', players, lastMarble)
  for mi in range(lastMarble):
    m = mi + 1

    if m % 23 == 0:
      curI = (curI - 7) % len(placed)
      removed = placed.pop(curI)
      scores[player] += m + removed
      assert curI < len(placed), 'bad modular arithmetic'
    else:
      curI, placed = place(placed, curI, m)

    player = (player + 1) % players

  print(max(scores.values()))

part1()
