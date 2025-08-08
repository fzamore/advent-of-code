from typing import Iterator

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

def getReplacementsFromRight(replacements: Replacements, start: str) -> Iterator[str]:
  for i in range(len(start), 0, -1):
    for src, dst in replacements:
      if start[i - len(src):i] == src:
        yield start[:i - len(src)] + dst + start[i:]

def part1() -> None:
  replacements, start = parse()
  print('start:', start)
  print(len(set(getReplacementsFromRight(replacements, start))))

def part2() -> None:
  replacements, target = parse()
  print('target:', len(target), target)

  reverseMap = [(y, x) for (x, y) in replacements]

  molecule = target
  steps = 0
  while molecule != 'e':
    molecule = next(getReplacementsFromRight(reverseMap, molecule))
    steps += 1
  print('done.')
  print(steps)

part2()
