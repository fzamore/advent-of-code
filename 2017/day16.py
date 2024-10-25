input = open('day16.txt').read()

Seq = list[str]

def spin(seq: Seq, x: int) -> None:
  nseq = seq[-x:] + seq[:-x]
  assert len(seq) == len(nseq), 'spin produced wrong-lengthed sequence'
  # Modify in-place for consistency with other operations.
  for i in range(len(seq)):
    seq[i] = nseq[i]

def exch(seq: Seq, a: int, b: int) -> None:
  t = seq[a]
  seq[a] = seq[b]
  seq[b] = t

def part(seq: Seq, a: str, b: str) -> None:
  exch(seq, seq.index(a), seq.index(b))

def execute(instrs: list[str], s: str) -> str:
  seq = list(s)
  for instr in instrs:
    match instr[0]:
      case 's':
        spin(seq, int(instr[1:]))
      case 'x':
        v = instr[1:].split('/')
        exch(seq, int(v[0]), int(v[1]))
      case 'p':
        v = instr[1:].split('/')
        part(seq, v[0], v[1])
  return ''.join(seq)

def part1() -> None:
  n = 16
  seq = [chr(ord('a') + i) for i in range(n)]

  instrs = input.split(',')
  print('instrs:', len(instrs))

  print(execute(instrs, ''.join(seq)))

def part2() -> None:
  n = 16
  seq = [chr(ord('a') + i) for i in range(n)]

  instrs = input.split(',')
  print('instrs:', len(instrs))

  orig = ''.join(seq)
  s = orig

  i = 0
  while True:
    s = execute(instrs, s)
    i += 1
    # This assumes that the algorithm will ultimately come back to the
    # original string (rather than a loop that starts somewhere other than
    # the beginning).
    if s == orig:
      print(s)
      break

  p = 1000000000
  r = p % i
  print('extra iterations:', r)
  for _ in range(r):
    s = execute(instrs, s)
  print(s)

part2()
