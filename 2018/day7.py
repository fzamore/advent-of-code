from collections import defaultdict

input = open('day7.txt').read().splitlines()

Dependencies = dict[str, set[str]]

def parseInput() -> tuple[set[str], Dependencies]:
  rdeps = defaultdict(list)
  deps = defaultdict(set)

  for line in input:
    v = line.split()
    v1 = v[1]
    v2 = v[7]
    rdeps[v1].append(v2)
    deps[v2].add(v1)
    if v2 not in rdeps:
      rdeps[v2] = []

  roots = set([k for k in rdeps if k not in deps])
  return roots, deps

def choose(deps: Dependencies) -> str:
  choices = []
  for k in deps:
    if len(deps[k]) == 0:
      choices.append(k)
  assert len(choices) > 0, 'could not find choice'
  return sorted(choices)[0]

def part1() -> None:
  roots, deps = parseInput()
  total = len(roots) + len(deps)
  print('roots:', roots)
  print('deps:', len(deps))
  print('total:', total)

  choices: list[str] = []
  while len(choices) < total:
    choice = sorted(roots)[0]
    choices.append(choice)
    roots.remove(choice)

    # Remove the choice from our dependencies and add any new roots.
    for k in deps:
      deps[k].discard(choice)
      if len(deps[k]) == 0:
        roots.add(k)

    for r in roots:
      assert len(deps[r]) == 0, 'roots should have no dependencies'
      del deps[r]

  print(''.join(choices))

def part2() -> None:
  roots, deps = parseInput()
  print('roots:', roots)
  print('deps:', len(deps))
  print(deps)

  dt = 60 if len(deps) == 22 else 0
  numWorkers = 5 if len(deps) == 22 else 2
  print('dt:', dt)
  print('numWorkers:', numWorkers)

  total = len(roots) + len(deps)
  print('total:', total)

  done: list[str] = []
  t = 0
  working: dict[int, tuple[str, int]] = {}
  while len(done) < total:
    # steps:
    #  if workers available, make choice and assign to workers
    #  for all active workers, determine if step is complete, and if so, add to choices, remove it from worker and from dependencies and add to roots
    #print('t:', t, working)

    for w in range(numWorkers):
      # Determine if any active workers have finished.
      if w in working:
        choice, end = working[w]
        if end > t:
          # Not done yet.
          continue

        # This worker is finished. Remove its work item and add its choice to our done list.
        print('done:', choice, w, t)
        del working[w]
        done.append(choice)

        # Update dependencies and roots.
        for k in deps:
          if choice in deps[k]:
            deps[k].remove(choice)
            if len(deps[k]) == 0:
              roots.add(k)

        for r in roots:
          assert len(deps[r]) == 0, 'roots should have no dependencies'
          del deps[r]

    # Each available worker should choose its next item.
    for w in range(numWorkers):
      if w not in working and len(roots) > 0:
        choice = sorted(roots)[0]
        roots.remove(choice)
        duration = dt + ord(choice) - ord('A') + 1
        working[w] = (choice, t + duration)
        print('starting:', choice, w, t, duration)

    # Increment timestep. We could probably increment by a greater amount
    # to be more efficient, but this is fast enough.
    t += 1

  print()
  print(''.join(done))
  print(t - 1)

part2()
