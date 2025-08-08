from heapq import heappop, heappush

data = open('day19.txt').read().splitlines()

Replacements = list[tuple[str, str]]

def parse() -> tuple[Replacements, str]:
  start = None
  replacements = []
  for line in data:
    if line == '':
      continue

    if '=>' not in line:
      assert start is None, 'multiple starts'
      start = line
      continue

    # Al => ThRnFAr
    v = line.split(' => ')
    assert len(v) == 2, 'bad line'
    replacements.append((v[0], v[1]))

  assert start is not None, 'did not find start'
  return replacements, start

def getReplacements(replacements: Replacements, start: str) -> set[str]:
  r = set()
  for src, dst in replacements:
    for i in range(len(start)):
      if start[i:i + len(src)] == src:
        r.add(start[:i] + dst + start[i + len(src):])
  return r

def part1() -> None:
  replacements, start = parse()
  print('start:', start)
  print(len(getReplacements(replacements, start)))

def part2() -> None:
  replacements, target = parse()
  print('target:', len(target), target)

  # This priority-queue based approach involves quite a bit of luck to
  # finish execution (and not choose a bad branch that will result in
  # indefinite spinning).

  reverseMap = [(y, x) for (x, y) in replacements]
  q: list[tuple[int, int, int, str]] = []
  # This insertion counter ensures that elements with tied priority get
  # popped off the queue in FIFO order. Without this, the code would spin
  # indefinitely. As far as I can tell, this is luck.
  inserts = 0
  heappush(q, (len(target), inserts, 0, target))
  while len(q) > 0:
    length, _, steps, node = heappop(q)
    assert length == len(node), 'bad queue management'

    if node == 'e':
      print('done.')
      print(steps)
      return

    # Sorting in the correct order with the correct key is a critical
    # piece as well. Without this, the code would spin indefinitely. As
    # far as I can tell, this is luck.
    reps = sorted(getReplacements(reverseMap, node), key=lambda x: (len(x), x), reverse=True)
    for rep in reps:
      inserts += 1
      heappush(q, (len(rep), inserts, steps + 1, rep))

  assert False, 'did not find answer'

part2()
