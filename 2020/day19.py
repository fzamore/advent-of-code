from common.io import readfile
import re
  
def parse(rules, ruleStr):
  if ruleStr in ['"a"', '"b"']:
    return ruleStr[1]

  if '|' in ruleStr:
    v = ruleStr.split(' | ')
    assert len(v) == 2, 'two many splits in rule: %s' % ruleStr
    return '(%s|%s)' % (parse(rules, v[0]), parse(rules, v[1]))

  result = ''
  values = ruleStr.split()
  for v in values:
    assert v.isdigit(), 'bad rule value: %s' % v
    result += parse(rules, rules[int(v)])
  return result

def part1():
  parsingRules = True
  rules = {}
  exprs = []
  for line in readfile('day19.txt'):
    if line == '':
      parsingRules = False
      continue

    if parsingRules:
      v = line.split(': ')
      rules[int(v[0])] =  v[1]
    else:
      exprs.append(line)

  print(rules)
  print(exprs)
  print()

  parsedRule0 = '^' + parse(rules, rules[0]) + '$'
  print(parsedRule0)

  prog = re.compile(parsedRule0)
  count = 0
  for expr in exprs:
    result = prog.match(expr) 
    if result != None:
      count += 1
    print(expr, result != None)
  print(count)

def part2():
  parsingRules = True
  rules = {}
  exprs = []
  for line in readfile('day19.txt'):
    if line == '':
      parsingRules = False
      continue

    if parsingRules:
      v = line.split(': ')
      rules[int(v[0])] =  v[1]
    else:
      exprs.append(line)

  # assume the following structure:
  #   0: 8 11
  #   8: 42
  #   11: 42 31
  # new rules:
  #   8: 42 | 42 8
  #   11: 42 31 | 42 11 31
  assert rules[0] == '8 11', 'bad rule 0: %s' % rules[0]
  assert rules[8] == '42', 'bad rule 8: %s' % rules[8]
  assert rules[11] == '42 31', 'bad rule 11: %s' % rules[11]
  assert parse(rules, rules[8]) == parse(rules, rules[42])
  rule42 = parse(rules, rules[42])
  rule31 = parse(rules, rules[31])
  
  # compile regexes that match the same number of occurrences of rule42 and rule31
  regexes = []
  for i in range(1, 10):
    regex = '^(%s+)%s{%d}%s{%d}$' % (rule42, rule42, i, rule31, i)
    regexes.append(re.compile(regex))

  count = 0
  for expr in exprs:
    for i in range(0, len(regexes)):
      r = regexes[i]
      result = r.match(expr)
      if result != None:
        count += 1
        print('match', i, expr)
        break
  print(count)
  
part2()
