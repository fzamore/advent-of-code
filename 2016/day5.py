from common.md5 import md5hash

input = open('day5.txt').read().rstrip()

def hash(s: str, i: int) -> str:
  return md5hash('%s%d' %(s, i))

def getNextChar(s: str, start: int = 0) -> tuple[int, str]:
  index = start
  while not (h := hash(s, index)).startswith('00000'):
    index += 1
  return index, h[5]

def getCharAndPosition(s: str, start: int) -> tuple[int, int, str]:
  index = start
  while True:
    while not (h := hash(s, index)).startswith('00000'):
      index += 1
    if h[5].isnumeric() and int(h[5]) < 8:
      return index, int(h[5]), h[6]
    index += 1

def part1() -> None:
  n = 8
  pwd: list[str] = []
  index = 0
  while len(pwd) < n:
    index, c = getNextChar(input, index)
    print('char:', index, c)
    pwd.append(c)

    index += 1

  print(''.join(pwd))

def part2() -> None:
  n = 8
  pwd: dict[int, str] = {}
  index = 0
  while len(pwd) < n:
    index, ci, c = getCharAndPosition(input, index)
    print('char:', index, ci, c)
    if ci not in pwd:
      pwd[ci] = c

    index += 1

  print(''.join([pwd[k] for k in range(n)]))

part2()
