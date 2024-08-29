input = open('day9.txt').read()[:-1]

# Parses a group of the given string starting at index i, and the most recent score prevScore.
def parseGroup(input: str, i: int, prevScore: int) -> tuple[int, int, int]:
  score = prevScore + 1
  assert input[i] == '{', 'group should start with {'
  i += 1
  inGarbage = False
  garbageCount = 0
  while True:
    match input[i]:
      case '{':
        if not inGarbage:
          # Start a new group.
          subscore, i, subgarbageCount = parseGroup(input, i, prevScore + 1)
          score += subscore
          garbageCount += subgarbageCount
        else:
          # If we're in garbage, { has no special meaning.
          garbageCount += 1
      case '}':
        if not inGarbage:
          # We're done with this group.
          return score, i, garbageCount
        else:
          garbageCount += 1
      case '<':
        if inGarbage:
          garbageCount += 1
        else:
          inGarbage = True
      case '!':
        # Skip the next character.
        i += 1
      case '>':
        inGarbage = False
      case _:
        if inGarbage:
          garbageCount += 1
        else:
          assert input[i] == ',', 'can only encounter commas if not in garbage'

    i += 1

def part1() -> None:
  print('len:', len(input))

  score, _, _ = parseGroup(input, 0, 0)
  print(score)

def part2() -> None:
  print('len:', len(input))

  _, _, garbageCount = parseGroup(input, 0, 0)
  print(garbageCount)

part2()

