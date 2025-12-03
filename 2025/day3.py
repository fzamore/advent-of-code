data = open('day3.txt').read().splitlines()

def findLargestJoltage(s: str, k: int) -> int:
  n = len(s)
  assert n >= k, 'string too short'
  start = 0
  end = n - k
  digits = []
  # Loop over the string once for each digit, from most to least
  # significant. Choose the largest digit in each pass such that the index
  # of each choice must be a/ greater than the previous choice and b/ far
  # enough from the end to leave enough digits for the remaining choices.
  for _ in range(k):
    choice = start
    for i, ch in enumerate(s):
      if start <= i <= end and int(ch) > int(s[choice]):
        choice = i
    digits.append(s[choice])
    start = choice + 1
    end += 1

  return int(''.join(digits))

def part1() -> None:
  print('lines:', len(data))
  ans = sum(findLargestJoltage(line, 2) for line in data)
  print(ans)

def part2() -> None:
  print('lines:', len(data))
  ans = sum(findLargestJoltage(line, 12) for line in data)
  print(ans)

part2()
