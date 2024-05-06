input = int(open('day14.txt').read())

def iterate(recipies: list[int], e1: int, e2: int) -> tuple[list[int], int, int]:
  v1, v2 = recipies[e1], recipies[e2]
  vn = v1 + v2
  assert vn < 20, 'bad iteration'
  if vn < 10:
    recipies.append(vn)
  else:
    # Append each digit.
    recipies.append(1)
    recipies.append(vn % 10)
  n = len(recipies)
  return recipies, (e1 + v1 + 1) % n, (e2 + v2 + 1) % n

def part1() -> None:
  print('input:', input)

  recipies = [3,7]
  e1, e2 = 0, 1
  while len(recipies) < input + 10:
    recipies, e1, e2 = iterate(recipies, e1, e2)

  print('results:', e1, e2)
  print(''.join(map(str, recipies[input:input + 10])))

# This is slow (15s).
def part2() -> None:
  print('input:', input)

  recipies = [3,7]
  e1, e2 = 0, 1
  last = 0
  n = len(str(input))
  m = 10 ** n
  print('n, m:', n, m)
  cmp = None
  while True:
    recipies, e1, e2 = iterate(recipies, e1, e2)
    while len(recipies) - last > n:
      if cmp is None:
        # Initialize value.
        cmp = int(''.join(map(str, recipies[last:last + n])))
      else:
        # Remove leftmost digit, shift digits left and add rightmost digit.
        cmp = ((cmp * 10) + recipies[last + n - 1]) % m

      assert cmp is not None, 'should have set cmp'
      if cmp == input:
        print('matching:', last)
        print(last)
        return
      last += 1

part2()
