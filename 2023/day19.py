from collections import namedtuple
from enum import Enum
from math import prod
from typing import Optional

input = open('day19.txt').read()

class Op(Enum):
  LT: int = 1
  GT: int = 2

Rule = namedtuple('Rule', ['category', 'op', 'value', 'dst'])
Workflow = namedtuple('Workflow', ['name', 'rules', 'dst'])
Part = dict
Rng = tuple[int, int] # inclusive

def parseRule(ruleStr: str) -> Optional[Rule]:
  if ':' not in ruleStr:
    # No condition.
    return None

  v = ruleStr.split(':')
  category = v[0][0]
  match v[0][1]:
    case '<':
      op = Op.LT
    case '>':
      op = Op.GT
    case _:
      assert False, 'bad rule: %s' % ruleStr
  value = int(v[0][2:])
  assert 1 <= value <= 4000, 'bad value'
  dst = v[1]
  return Rule(category, op, value, dst)

def parseWorkflow(workflowStr: str) -> Workflow:
  v = workflowStr.split('{')
  assert len(v) == 2, 'bad workflow str: %s' % workflowStr
  name = v[0]
  rules = []
  dst = v[1].split(',')[-1][:-1]
  for ruleStr in v[1][:-1].split(','):
    rule = parseRule(ruleStr)
    if rule is not None:
      rules.append(rule)
  return Workflow(name, rules, dst)

def parsePart(partStr: str) -> Part:
  v = partStr[1:-1].split(',')
  part = {}
  for s in v:
    values = s.split('=')
    part[values[0]] = int(values[1])
  return part

def getNextWorkflow(part: Part, workflow: Workflow) -> str:
  for rule in workflow.rules:
    c = rule.category
    match rule.op:
      case Op.LT:
        if part[c] < rule.value:
          return rule.dst
      case Op.GT:
        if part[c] > rule.value:
          return rule.dst
      case _:
        assert False, 'bad op'
  return workflow.dst

# Returns true if accepted, false if rejected.
def tracePart(workflows: dict[str, Workflow], part: Part) -> bool:
  dst = 'in'
  while dst not in ['A', 'R']:
    workflow = workflows[dst]
    dst = getNextWorkflow(part, workflow)
  return dst == 'A'

def intersectRanges(r1: Rng, r2: Rng) -> Optional[Rng]:
  start = max(r1[0], r2[0])
  end = min(r1[1], r2[1])
  if start > end:
    return None
  return (start, end)

def iterateWorkflow(
  workflowName: str,
  workflows: dict[str, Workflow],
  rngs: dict[str, Rng],
) -> int:
  print('processing workflow', workflowName, rngs)

  if workflowName == 'R':
    # reject
    return 0

  if workflowName == 'A':
    # accept. multiply all range sizes together
    return prod([rngs[c][1] - rngs[c][0] + 1 for c in rngs])

  result = 0
  workflow = workflows[workflowName]
  for rule in workflow.rules:
    c = rule.category
    rng = rngs[c]
    if rule.op == Op.LT:
      assert rule.value > 1, '< 1 not yet implemented'
      ruleRng1 = (1, rule.value - 1)
      ruleRng2 = (rule.value, 4000)
    else:
      assert rule.value < 4000, '> 4000 not yet implemented'
      ruleRng1 = (rule.value + 1, 4000)
      ruleRng2 = (1, rule.value)

    i1 = intersectRanges(rng, ruleRng1)
    if i1 is not None:
      # the rule matched. follow it
      rngs1 = rngs.copy()
      rngs1[c] = i1
      result += iterateWorkflow(rule.dst, workflows, rngs1)

    i2 = intersectRanges(rng, ruleRng2)
    if i2 is not None:
      # update our ranges and continue to the next rule
      rngs[c] = i2

  # process the workflow destination range
  result += iterateWorkflow(workflow.dst, workflows, rngs)
  return result

def part1() -> None:
  workflowsStr, partsStr = input.split("\n\n")
  workflows = {}
  for workflowStr in workflowsStr.splitlines():
    workflow = parseWorkflow(workflowStr)
    workflows[workflow.name] = workflow
  parts = [parsePart(x) for x in partsStr.splitlines()]
  print(workflows)
  print(parts)

  r = 0
  for part in parts:
    if tracePart(workflows, part):
      print('accepted', part)
      r += sum(part.values())
  print(r)

def part2() -> None:
  workflowsStr = input.split("\n\n")[0]
  workflows = {}
  for workflowStr in workflowsStr.splitlines():
    workflow = parseWorkflow(workflowStr)
    workflows[workflow.name] = workflow

  print('workflow count:', len(workflows))

  maxV = 4000
  rngs = {
    'x': (1, maxV),
    'm': (1, maxV),
    'a': (1, maxV),
    's': (1, maxV),
  }
  start = 'in'
  print(workflows[start])
  print()
  print(iterateWorkflow(start, workflows, rngs))

part2()
