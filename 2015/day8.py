data = open('day8.txt').read().splitlines()

def countData(s: str) -> int:
  assert s[0] == '"' and s[-1] == '"', 'bad str'
  count = 0
  i = 1
  while i < len(s) - 1:
    ch = s[i]
    if ch == '\\':
      i += 1
      ch = s[i]
      match ch:
        case '\\' | '"':
          pass
        case 'x':
          i += 2
        case _:
          assert False, 'bad escape seq'

    count += 1
    i += 1
  return count

def encode(s: str) -> str:
  assert s[0] == '"' and s[-1] == '"', 'bad str'
  chars = ['"']
  for ch in s:
    if ch in ['\\', '"']:
      chars.append('\\')
    chars.append(ch)
  chars.append('"')
  return ''.join(chars)

def part1() -> None:
  print('input:', len(data))
  totalCodeCount, totalDataCount = 0, 0
  for s in data:
    totalCodeCount += len(s)
    totalDataCount += countData(s)
  print(totalCodeCount - totalDataCount)

def part2() -> None:
  totalCodeCount, totalEncodedCodeCount = 0, 0
  for s in data:
    e = encode(s)
    print('s:', s, e, len(s), len(e))
    totalCodeCount += len(s)
    totalEncodedCodeCount += len(e)
  print(totalEncodedCodeCount - totalCodeCount)

part2()
