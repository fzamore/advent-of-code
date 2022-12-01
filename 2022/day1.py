from common.readfile import readfile

def day1():
  a = [0]
  for line in readfile('day1.txt'):
    if line == '':
      a.append(0)
    else:
      a[-1] += int(line)

  print(max(a))

def day2():
  a = [0]
  for line in readfile('day1.txt'):
    if line == '':
      a.append(0)
    else:
      a[-1] += int(line)

  print(sum(sorted(a, reverse=True)[0:3]))

day2()
