from math import ceil, floor, prod, sqrt

input = open('day6.txt').read().splitlines()

def computeNumberOfWaysToWin(t: int, d: int) -> int:
  # d = (t - x)x
  # x^2 - tx + d = 0
  # x = (t +- sqrt(t^2 - 4d))/2

  determinant = t * t - 4 * d
  assert determinant >= 0, 'bad determinant: %d %d' % (t, d)

  x1 = (t + sqrt(determinant)) / 2
  x2 = (t - sqrt(determinant)) / 2
  x1r = ceil(x1) - 1
  x2r = floor(x2) + 1
  count = x1r - x2r + 1
  print(t, d, x1, x2, x1r, x2r, count)
  return count

def part1():
  times = list(map(int, input[0].split()[1:]))
  distances = list(map(int, input[1].split()[1:]))
  print(times, distances)
  print(len(times))
  assert len(times) == len(distances), 'bad input'

  values = []
  for i in range(len(times)):
    t = times[i]
    d = distances[i]
    count = computeNumberOfWaysToWin(t, d)
    values.append(count)
  print(prod(values))

def part2():
  time = int(''.join(input[0].split()[1:]))
  distance = int(''.join(input[1].split()[1:]))
  print(time, distance)

  print(computeNumberOfWaysToWin(time, distance))

part2()
