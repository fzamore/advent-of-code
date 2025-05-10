data = open('day7.txt').read().splitlines()

Wires = dict[str, int]

def execute(wires: Wires, instr: str) -> None:
  def r(w: str) -> int:
    if w.isnumeric():
      return int(w)
    return wires[w]

  v = instr.split()
  dst = v[-1]

  if 'AND' in v:
    a = r(v[0]) & r(v[2])
  elif 'OR' in v:
    a = r(v[0]) | r(v[2])
  elif 'LSHIFT' in v:
    a = r(v[0]) << int(v[2])
  elif 'RSHIFT' in v:
    a = r(v[0]) >> int(v[2])
  elif 'NOT' in v:
    a = ~r(v[1])
  else:
    assert len(v) == 3, 'bad instr'
    a = r(v[0])

  wires[dst] = a & (2 ** 16 - 1)

def canExecute(wires: Wires, instr: str) -> bool:
  v = instr.split()
  dst = v[-1]
  if dst in wires:
    # We already have the destination value. Skip.
    return False

  # Find which instruction indicies are required to have values.
  if any([k in v for k in ['AND', 'OR', 'LSHIFT', 'RSHIFT']]):
    indicies = [0, 2]
  elif 'NOT' in v:
    indicies = [1]
  else:
    indicies = [0]

  return all([v[i].isnumeric() or (v[i] in wires) for i in indicies])

def executeAll(initial: Wires = {}) -> Wires:
  wires = initial.copy()
  while 'a' not in wires:
    for instr in data:
      if canExecute(wires, instr):
        execute(wires, instr)
  return wires

def part1() -> None:
  print('instrs:', len(data))
  wires = executeAll()
  print(wires['a'])

def part2() -> None:
  print('instrs:', len(data))
  wires = executeAll()
  print('"a" wire after initial run:', wires['a'])
  wires = executeAll({'b': wires['a']})
  print(wires['a'])

part2()
