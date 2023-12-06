from math import ceil, floor, prod, sqrt


input = open('day6.txt').read().splitlines()

def part1():
  times = list(map(int, input[0].split()[1:]))
  distances = list(map(int, input[1].split()[1:]))
  print(times, distances)
  print(len(times))
  assert len(times) == len(distances), 'bad input'

  # d = (t - x)x
  # x^2 - tx + d = 0
  # x = (t +- sqrt(t^2 - 4d))/2

  values = []
  for i in range(len(times)):
    t = times[i]
    d = distances[i]

    determinant = t * t - 4 * d
    assert determinant >= 0, 'bad determinant: %d %d' % (t, d)

    x1 = (t + sqrt(determinant)) / 2
    x2 = (t - sqrt(determinant)) / 2
    x1r = ceil(x1) - 1
    x2r = floor(x2) + 1
    count = x1r - x2r + 1
    print(t, d, x1, x2, x1r, x2r, count)

    values.append(count)
  print(prod(values))


part1()
