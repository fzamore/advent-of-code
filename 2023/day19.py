from collections import namedtuple
from enum import Enum
from typing import Optional

input = open('day19.txt').read()

class Op(Enum):
  LT: int = 1
  GT: int = 2

Rule = namedtuple('Rule', ['category', 'op', 'value', 'dst'])
Workflow = namedtuple('Workflow', ['name', 'rules', 'dst'])
Part = dict

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

part1()
