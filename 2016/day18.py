input = open('day18.txt').read().rstrip()

def getNextRow(row: list[bool], n: int) -> list[bool]:
  nextRow = []
  for i in range(n):
    # Stolen from Reddit. The center tile doesn't matter. The new tile is
    # a trap iff the left tile and right tile differ.
    leftTile = row[i - 1] if i > 0 else False
    rightTile = row[i + 1] if i < n - 1 else False
    nextRow.append(leftTile != rightTile)
  return nextRow

def countSafeSpots(numRows: int) -> int:
  safes = 0
  row = [ch == '^' for ch in input]
  n = len(row)
  print('row size:', n)

  for _ in range(numRows):
    safes += row.count(False)
    row = getNextRow(row, n)
  return safes

def part1() -> None:
  print(countSafeSpots(40))

def part2() -> None:
  print(countSafeSpots(400000))

part2()
