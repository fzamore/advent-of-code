from collections import defaultdict

input = open('day7.txt').read().splitlines()

def computeDirSizes(input) -> dict[str, int]:
  # Keep track of the current cwd stack. Whenever we encounter a file, add
  # its size to each directory in the cwd stack.
  cwdstack: list[str] = []
  sizes: dict[str, int] = defaultdict(int)
  for line in input:
    match line.split():
      case ['$', 'ls']: pass
      case ['$', 'cd', '/']: cwdstack = ['/']
      case ['$', 'cd', '..']: cwdstack.pop()
      case ['$', 'cd', dir]: cwdstack.append(dir)
      case ['dir', _]: pass
      case [size, _]:
        for i in range(0, len(cwdstack)):
          # compute prefixes for each dir
          sizes['/'.join(cwdstack[:i+1])] += int(size)
  return sizes

def part1():
  sizes = computeDirSizes(input)
  print(sum([s for s in sizes.values() if s <= 100000]))

def part2():
  sizes = computeDirSizes(input)

  maximum = 70000000
  unused = 30000000
  needed = maximum - sizes['/']
  assert needed < unused, 'premise of puzzle is faulty'

  print(min([s for s in sizes.values() if s >= unused - needed]))

part2()
