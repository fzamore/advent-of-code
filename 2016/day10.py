from common.ints import ints
from collections import defaultdict

input = open('day10.txt').read().splitlines()

# bot -> values that go to that bot
Bots = dict[int, list[int]]

# bot -> low dst, high dst, is low dst output, is high output
Instrs = dict[int, tuple[int, int, bool, bool]]

def parseInput() -> tuple[Bots, Instrs]:
  bots, instrs = defaultdict(list), {}
  for line in input:
    if 'value' in line:
      v, b = ints(line)
      bots[b].append(v)
    else:
      src, low, high = ints(line)
      isOutputLow = 'low to output' in line
      isOutputHigh = 'high to output' in line
      assert src not in instrs
      instrs[src] = (
        low,
        high,
        isOutputLow,
        isOutputHigh,
      )
  return bots, instrs

def execute(bots: Bots, instrs: Instrs, *, isPart1: bool) -> int:
  outputs = {}

  q = []
  for b in bots:
    # We start with bots that have only two values.
    if len(bots[b]) == 2:
      q.append(b)

  print('initial q:', len(q))
  while len(q) > 0:
    b = q.pop(0)
    assert len(bots[b]) == 2, 'bot should only have two values to be processed'
    assert b in instrs, 'bot missing from instrs'
    instrLow, instrHigh, isOutputLow, isOutputHigh = instrs[b]
    botLow, botHigh = min(bots[b]), max(bots[b])

    print('processing:', b, instrLow, instrHigh, isOutputLow, isOutputHigh, botLow, botHigh)

    if isPart1 and botLow == 17 and botHigh == 61:
      return b

    bots[b] = []
    if isOutputLow:
      assert instrLow not in outputs, 'should not have already seen output low'
      outputs[instrLow] = botLow
    else:
      bots[instrLow].append(botLow)
      if len(bots[instrLow]) == 2:
        q.append(instrLow)

    if isOutputHigh:
      assert instrHigh not in outputs, 'should not have already seen output high'
      outputs[instrHigh] = botHigh
    else:
      bots[instrHigh].append(botHigh)
      if len(bots[instrHigh]) == 2:
        q.append(instrHigh)

  print('outputs:', outputs)
  assert not isPart1, 'should be part 2'
  return outputs[0] * outputs[1] * outputs[2]

def part1() -> None:
  bots, instrs = parseInput()
  print('data:', len(bots), len(instrs))
  print(execute(bots, instrs, isPart1=True))

def part2() -> None:
  bots, instrs = parseInput()
  print('data:', len(bots), len(instrs))
  print(execute(bots, instrs, isPart1=False))

part2()
