input = open('day12.txt').read().splitlines()

State = dict[int, str]
Rule = str

def parseInput() -> tuple[State, list[Rule]]:
  raw = input[0].split(': ')[1]
  state = dict(zip(range(len(raw)), raw))
  print('initial:', len(state))
  print(state)

  rules = []
  for line in input[2:]:
    rules.append(line)

  return state, rules

def doesRuleMatch(state: State, i: int, rule: Rule) -> bool:
  for j in range(5):
    if state.get(i + j - 2, '.') != rule[j]:
      return False
  return True

def iterate(state: State, rules: list[Rule]) -> State:
  mn = min(state.keys()) - 5
  mx = max(state.keys()) + 5
  next = {}
  for i in range(mn, mx):
    for r in rules:
      if doesRuleMatch(state, i, r):
        next[i] = r[9]
        break
    else:
      next[i] = '.'

  # Trim both ends of the state.
  i = mn
  while next[i] == '.':
    del next[i]
    i += 1

  i = mx - 1
  while next[i] == '.':
    del next[i]
    i -= 1

  return next

def value(state: State) -> int:
  ans = 0
  for k in state:
    if state[k] == '#':
      ans += k
  return ans

def part1() -> None:
  state, rules = parseInput()

  n = 20
  for _ in range(n):
    state = iterate(state, rules)
  print('done')
  print(value(state))

def part2() -> None:
  state, rules = parseInput()

  # Testing whether the pattern holds.
  # n = 20000 # 2181166
  # n = 2000 # 219166
  # n = 500 # 55666
  # n = 5000 # 546166

  n = 50000000000

  # The sentinel was found by inspection. After a while, the score
  # increases by a constant amount each iteration.
  sentinel = 109

  values = {}
  values[-1] = 0

  first = None

  for i in range(n):
    state = iterate(state, rules)
    v = value(state)
    values[i] = v
    d = v - values[i - 1]
    if d == sentinel:
      first = i
      break

  assert first is not None, 'did not find first instance of pattern'
  print('done', first)

  ans = values[first - 1] + sentinel * (n - first)
  print(ans)

part2()
