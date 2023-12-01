input = open('day1.txt').read().splitlines()

numbers = {
  'one': 1,
  'two': 2,
  'three': 3,
  'four': 4,
  'five': 5,
  'six': 6,
  'seven': 7,
  'eight': 8,
  'nine': 9,
}

def parseLine(line: str) -> list[int]:
  result = []
  for i in range(len(line)):
    if line[i].isdigit():
      result.append(int(line[i]))
    for s in numbers:
      if line[i:i + len(s)] == s:
        result.append(numbers[s])
  assert len(result) > 0, 'did not find any numbers in line: %s' % line
  return result

def part1():
  sum = 0
  for line in input:
    numbers = [x for x in line if x.isdigit()]
    all = ''.join(numbers)
    assert len(all) > 0, 'bad line: %s' % all
    s = all[0] + all[-1]
    n = int(s)
    assert n >= 10 and n <= 99, 'bad string: %s' % s
    print(n)
    sum += n

  print(sum)

def part2():
  sum = 0
  for line in input:
    digits = parseLine(line)
    d1, d2 = digits[0], digits[-1]
    assert d1 > 0 and d1 < 10, 'bad digit: %s' % d1
    assert d2 > 0 and d2 < 10, 'bad digit: %s' % d2
    n = d1 * 10 + d2
    print(line, d1, d2, n)
    sum += n
  print(sum)

part2()
