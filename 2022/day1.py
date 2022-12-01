from common.readfile import readfile
from collections import defaultdict

def day1():
  d = defaultdict(int)
  e = 0
  for line in readfile('day1.txt'):
    if line == '':
      e += 1
    else:
      d[e] += int(line)

  print(max(d.values()))

def day2():
  d = defaultdict(int)
  e = 0
  for line in readfile('day1.txt'):
    if line == '':
      e += 1
    else:
      d[e] += int(line)

  v = sorted(d.values(), reverse=True)
  print(sum(v[0:3]))

day2()
