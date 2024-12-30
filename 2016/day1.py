from common.arraygrid import Delta, turnRight, turnLeft

input = open('day1.txt').read().split(', ')

def turn(delta: Delta, inst: str) -> Delta:
  dir = inst[0]
  assert dir in ['L', 'R'], 'bad inst'
  return turnRight(delta) if dir == 'R' else turnLeft(delta)

def part1() -> None:
  x, y = 0, 0
  dx, dy = 0, -1
  for inst in input:
    dx, dy = turn((dx, dy), inst)
    qty = int(inst[1:])
    x += dx * qty
    y += dy * qty
  print('end:', x, y)
  print(abs(x) + abs(y))

def part2() -> None:
  x, y = 0, 0
  dx, dy = 0, -1
  seen = set()
  for inst in input:
    dx, dy = turn((dx,dy), inst)
    qty = int(inst[1:])

    for _ in range(qty):
      x += dx
      y += dy

      if (x, y) in seen:
        print('end:', x, y)
        print(abs(x) + abs(y))
        return

      seen.add((x, y))

part2()
