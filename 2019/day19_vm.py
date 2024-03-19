from intcode import IntcodeVM

input = open('day19.txt').read().split(',')

def inBeam(x: int, y: int) -> bool:
  return IntcodeVM.initFromInput(input).addInputs([x, y]).runAll()[0] == 1

def part1() -> None:
  result = 0
  for x in range(50):
    for y in range(50):
      outputs = IntcodeVM.initFromInput(input).addInputs([x, y]).runAll()
      assert len(outputs) == 1, 'bad output'
      result += outputs[0]
  print(result)

def part2() -> None:
  start = 7, 9 # found by printing out the tractor beam pattern
  print('start:', start)
  sx, sy = start
  rows = {sy: sx}
  row = sy
  size = 100

  # For each row, calculate the max column within the beam.
  while True:
    mx = rows[row]
    row += 1

    newMax = mx
    while inBeam(newMax, row):
      newMax += 1
    # We went beyond the beam, so course-correct by 1.
    newMax -= 1

    rows[row] = newMax

    # Assume this coordinate is the top right of the square. If the bottom
    # left of the correctly-sized square is also in the beam, then we have
    # our answer.
    newRow = row + size - 1
    newCol = newMax - size + 1
    if inBeam(newCol, newRow):
      print('done:', newCol, row)
      print(10000 * newCol + row)
      break

part2()
