data = open('day1.txt').read().strip()

def part1() -> None:
  ans = 0
  for c in data:
    if c == '(': ans += 1
    elif c == ')': ans -= 1
    else: assert False, 'bad char'
  print(ans)

def part2() -> None:
  floor = 0
  for i, c in enumerate(data):
    if c == '(': floor += 1
    elif c == ')': floor -= 1
    else: assert False, 'bad char'
    if floor == -1:
      print(i + 1)
      return
  assert False, 'did not find basement'

part2()
