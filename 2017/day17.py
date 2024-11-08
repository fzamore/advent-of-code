input = open('day17.txt').read()

def part1() -> None:
  steps = int(input)
  print('steps:', steps)
  buf = [0]
  pos = 0

  n = 2017
  for i in range(n):
    pos = (pos + steps) % len(buf) + 1
    buf.insert(pos, i + 1)

  assert buf[pos] == n
  print('pos:', pos)
  print(buf[pos + 1])

def part2() -> None:
  steps = int(input)
  print('steps:', steps)
  pos = 0

  n = 50000000
  # Assume the value that ends up at index 1 is what we want.
  ans = 0
  m = 1
  for i in range(n):
    pos = (pos + steps) % m + 1
    if pos == 1:
      # Update the element stored at index 1.
      ans = i + 1
    # Increase the modulus by 1 to simulate a new entry into the buffer
    # each time.
    m += 1

  print('pos:', pos)
  print(ans)

part2()
