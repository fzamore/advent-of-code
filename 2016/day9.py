from common.ints import ints

input = open('day9.txt').read().strip()

# Advances past one "group" of characters, without considering any
# subgroups. If there is no marker, it only advances a single character.
# Otherwise, it advances the number of characters specified in the marker.
# Returns a triplet of (
#   index of the first non-marker character,
#   length of the repeated section,
#   number of repeats
# )
def advance(s: str, start: int) -> tuple[int, int, int]:
  if s[start] != '(':
    # This is a normal character.
    return start, 1, 1

  markerEnd = s.find(')', start)
  assert markerEnd is not None and markerEnd > start, 'malformed input'
  length, repeats = ints(s[start:markerEnd + 1])
  return markerEnd + 1, length, repeats

# Advances past one group of characters, but considers subgroups.
# Returns a pair of (index after the entire group, total decompressed length of the group)
def advance2(s: str, start: int) -> tuple[int, int]:
  # First, advance past a single group.
  afterMarker, length, repeats = advance(s, start)
  afterGroup = afterMarker + length

  # Iterate through the group to check for any markers within the group.
  total = 0
  i = afterMarker
  while i < afterGroup:
    if s[i] == '(':
      # We have a marker. Recur to parse this group.
      i, subtotal = advance2(s, i)
      total += subtotal
    else:
      # Normal character.
      i += 1
      total += 1
  return i, total * repeats

def part1() -> None:
  print('input:', len(input))
  assert len(input.splitlines()) == 1, 'input should be one line'
  i = 0
  total = 0
  while i < len(input):
    afterMarker, length, repeats = advance(input, i)
    i = afterMarker + length
    total += length * repeats

  print(total)

def part2() -> None:
  print('input:', len(input))
  assert len(input.splitlines()) == 1, 'input should be one line'
  i = 0
  total = 0
  while i < len(input):
    i, subtotal = advance2(input, i)
    total += subtotal

  print(total)

part2()
