from collections import defaultdict

input = open('day22.txt').read().splitlines()

def step(n: int) -> int:
  m = 16777216
  n = (n ^ (n * 64)) % m
  n = (n ^ (n // 32)) % m
  n = (n ^ (n * 2048)) % m
  return n

def part1() -> None:
  n = 2000
  ans = 0
  for line in input:
    secretNumber = int(line)
    for _ in range(n):
      secretNumber = step(secretNumber)
    ans += secretNumber
  print(ans)

def part2() -> None:
  n = 2000

  pricesBySeq: dict[tuple[int, int, int, int], int] = defaultdict(int)

  print('size:', len(input))

  for line in input:
    secretNumber = int(line)
    last = secretNumber
    changes = []
    digits = []
    for _ in range(n):
      digits.append(secretNumber % 10)
      secretNumber = step(secretNumber)
      changes.append((secretNumber % 10) - (last % 10))
      last = secretNumber

    seen = set()
    for i in range(len(changes) - 4):
      seq = tuple(changes[i:i + 4])
      assert len(seq) == 4, 'bad seq'
      if seq not in seen:
        seen.add(seq)
        pricesBySeq[seq] += digits[i + 4]

  print('number of sequences:', len(pricesBySeq))
  print(max(pricesBySeq.values()))

part2()
