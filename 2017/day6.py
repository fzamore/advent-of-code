input = open('day6.txt').read()

def iterate(banks: list[int]) -> None:
  # Find the index of the largest bank (choose lowest index in case of a tie).
  choice = banks.index(max(banks))

  v = banks[choice]
  banks[choice] = 0

  m = len(banks)
  all = v // len(banks)
  rem = v % len(banks)

  # Decrease all banks by the quotient.
  for i in range(len(banks)):
    banks[i] += all

  # For the remainder, decrease by one in order until we use up the remainder.
  for i in range(rem):
    banks[(choice + 1 + i) % m] += 1

def part1() -> None:
  banks = list(map(int, input.split()))
  print('banks:', len(banks))
  print(banks)

  seen = set()
  i = 0
  while tuple(banks) not in seen:
    seen.add(tuple(banks))
    iterate(banks)
    i += 1
  print(i)

def part2() -> None:
  banks = list(map(int, input.split()))
  print('banks:', len(banks))
  print(banks)

  seen = {}
  i = 0
  while tuple(banks) not in seen:
    seen[tuple(banks)] = i
    iterate(banks)
    i += 1
  print(i - seen[tuple(banks)])

part2()
