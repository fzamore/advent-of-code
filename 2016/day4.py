from common.ints import ints
from collections import Counter, defaultdict

input = open('day4.txt').read().splitlines()

def parseLine(line: str) -> tuple[str, int, str]:
  lastDashi = -1
  for i, ch in enumerate(line):
    if ch == '-':
      lastDashi = i

  encrypted = line[:lastDashi].replace('-', '')
  id = -ints(line)[0]
  checksum = line[line.find('[') + 1:line.find(']')]
  assert len(checksum) == 5, 'bad checksum'

  return encrypted, id, checksum

def isReal(line: str) -> bool:
  encrypted, _, checksum = parseLine(line)

  counts = Counter(encrypted)
  rcounts = defaultdict(list)
  for ch, cn in counts.most_common():
    rcounts[cn].append(ch)

  actual = []
  for cn in sorted(rcounts.keys(), reverse=True):
    actual.extend(sorted(rcounts[cn]))
  actual = actual[:5]
  return ''.join(actual) == checksum

def decrypt(encrypted: str, id: int) -> str:
  decrypted = []
  for ech in encrypted:
    if ech == '-':
      dch = ' '
    else:
      dch = chr(ord('a') + (ord(ech) - ord('a') + id) % 26)
    decrypted.append(dch)
  return ''.join(decrypted)

def part1() -> None:
  ans = 0
  for line in input:
    if isReal(line):
      print('real:', line)
      _, id, _ = parseLine(line)
      ans += id
  print(ans)

def part2() -> None:
  for line in input:
    encrypted, id, _ = parseLine(line)
    decrypted = decrypt(encrypted, id)
    if 'north' in decrypted:
      print('match:', decrypted)
      print(id)

part2()
