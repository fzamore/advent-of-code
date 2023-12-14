from common.arraygrid import ArrayGrid

input = open('day14.txt').read().splitlines()

def initGrid() -> ArrayGrid:
  grid = ArrayGrid(len(input[0]), len(input))
  for y, line in enumerate(input):
    for x, c in enumerate(line):
      grid.setValue(x, y, c)
  return grid

def part1():
  grid = initGrid()
  w, h = grid.getWidth(), grid.getHeight()
  print('grid: %d x %d' % (w, h))

  grid.print2D()

  count = 0
  for x in range(w):
    dst = -1
    for y in range(h):
      c = grid.getValue(x, y)
      if c == '.' and dst == -1:
        dst = y
      elif c == '#':
        dst = y + 1
      elif c == 'O':
        count += 1
        if dst != -1 and dst < y:
          # move up
          assert grid.getValue(x, dst) == '.', \
            'bad spot to move: %d %d %d' % (x, y, dst)
          grid.setValue(x, dst, 'O')
          grid.setValue(x, y, '.')
          dst += 1
        else:
          dst = y + 1
  grid.print2D()

  print('rocks:', count)

  count2 = 0
  load = 0
  for x in range(w):
    for y in range(h):
      if grid.getValue(x, y) == 'O':
        load += h - y
        count2 += 1

  print(load)
  assert count == count2, 'bad rock moving: %d, %d' % (count, count2)




part1()

