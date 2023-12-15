input = open('day15.txt').read().splitlines()[0].split(',')

def algo(s: str) -> int:
  acc = 0
  for c in s:
    acc += ord(c)
    acc *= 17
    acc %= 256
  return acc

def findInBox(box: list[tuple[str, int]], label: str) -> int:
  for i, e in enumerate(box):
    if e[0] == label:
      return i
  return -1

def add(boxes: list[list[tuple[str, int]]], label: str, f: int) -> None:
  box = boxes[algo(label)]
  index = findInBox(box, label)
  if index > -1:
    box[index] = (label, f)
  else:
    box.append((label, f))

def remove(boxes: list[list[tuple[str, int]]], label: str) -> None:
  box = boxes[algo(label)]
  index = findInBox(box, label)
  if index > -1:
    box.pop(index)

def printBoxes(boxes: list[list[tuple[str, int]]]) -> None:
  print()
  print('Boxes:')
  for i, e in enumerate(boxes):
    if len(e) > 0:
      print('  %d: %s' % (i, e))
  print()

def part1():
  print(sum([algo(s) for s in input]))

def part2():
  boxes = []
  for _ in range(256):
    boxes.append([])
  for s in input:
    if '=' in s:
      v = s.split('=')
      label = v[0]
      f = int(v[1])
      box = algo(label)
      print('add', label, f, box)
      add(boxes, label, f)
    else:
      assert s[-1] == '-', 'bad input'
      label = s[:-1]
      box = algo(label)
      print('remove', label, box)
      remove(boxes, label)
  printBoxes(boxes)

  power = 0
  for i, box in enumerate(boxes):
    for slot, (label, f) in enumerate(box):
      power += (i + 1) * (slot + 1) * f
  print(power)

part2()
