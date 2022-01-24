from common.io import readfile

def step(cups, curi):
  cupsLen = len(cups)
  cur = cups[curi]
  r1 = (curi + 1) % len(cups)
  r2 = (curi + 4) % len(cups)
  assert r1 != r2, 'bad index computation: %d, (%d, %d)' % (curi, r1, r2)
  if r1 < r2:
    removed = cups[r1:r2]
    cups = cups[:r1] + cups[r2:]
  else:
    removed = cups[r1:] + cups[:r2]
    cups = cups[r2:r1]
  assert len(removed) == 3, 'bad removed computation: %d, (%d, %d)' % (curi, r1, r2)
  assert len(cups) == cupsLen - 3, 'bad cups computation: %d, (%d, %d)' % (curi, r1, r2)

  dest = ((cur - 2) % cupsLen) + 1
  while dest not in cups:
    dest = ((dest - 2) % cupsLen) + 1
  desti = cups.index(dest)
  cups = cups[:(desti + 1)] + removed + cups[(desti + 1):]
  newcuri = (cups.index(cur) + 1) % cupsLen
  return cups, newcuri

def step2(cups, cur):
  cupsLen = len(cups) - 1
  curP, curN = cups[cur]

  # three cups to remove
  c1 = curN
  _, c2 = cups[c1]
  _, c3 = cups[c2]
  _, c4 = cups[c3]
  cups[cur] = (curP, c4)
  cups[c4] = (cur, cups[c4][1])

  # subtract 1 (1-indexed) from current
  dest = ((cur - 2) % cupsLen) + 1
  while dest in [c1, c2, c3]:
    dest = ((dest - 2) % cupsLen) + 1

  # insert three cups after destination cup
  destP, destN = cups[dest]
  _, destNN = cups[destN]
  cups[dest] = (destP, c1)
  cups[destN] = (c3, destNN)
  cups[c1] = (dest, c2)
  cups[c3] = (c2, destN)

  # new current cup is next after current cup
  return cups[cur][1]

def part1():
  cups = [int(x) for x in readfile('day23.txt')[0]]
  print('initial cups', cups)

  n = 100
  curi = 0
  for i in range(0, n):
    cups, curi = step(cups, curi)
    print()
    print('after step', i + 1, cups, curi)

  ansi = cups.index(1)
  ans = cups[(ansi + 1):] + cups[:ansi]
  assert len(ans) == 8, 'bad ans calculation'
  print(''.join([str(x) for x in ans]))

def part2():
  # `cups` is a 1-indexed array where each index stores a tuple with the 
  # (next, prev) cup for that label, in clockwise order. Essentially, 
  # a linked list stored in an array indexed by cup label.
  # cups[0] is always None

  values = [int(x) for x in readfile('day23.txt')[0]]
  maxCup = 1000000
  # add one so we can maintain 1-indexing
  cups = [None] * (maxCup + 1)
  l = len(values)
  for i in range(1, l - 1):
    cups[values[i]] = (values[i - 1], values[i + 1])
  
  # add extra cups
  cups[values[l - 1]] = (values[l - 2], max(values) + 1)
  cups[max(values) + 1] = (values[l - 1], max(values) + 2)
  for i in range(max(values) + 2, maxCup):
    cups[i] = (i - 1, i + 1)

  cups[values[0]] = (maxCup, values[1])
  cups[maxCup] = (maxCup - 1, values[0])

  cur = values[0]
  
  n = 10000000
  for i in range(0, n):
    cur = step2(cups, cur)
  
  oneN = cups[1][1]
  oneNN = cups[oneN][1]
  print(oneN, oneNN, oneN * oneNN)

part2()
