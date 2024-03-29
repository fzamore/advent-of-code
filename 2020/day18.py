from common.readfile import readfile
import math

def evaluate(expr):
    if isinstance(expr, int):
        return expr
    assert isinstance(expr, list), 'bad expr: %s' % expr

    result = evaluate(expr[0])
    i = 1
    while i < len(expr):
        op = expr[i]
        i += 1
        assert op in ['+', '*'], 'expected operator: %s' % op

        opnd = evaluate(expr[i])
        i += 1
        match op:
            case '+':
                result += opnd
            case '*':
                result *= opnd
            case _:
                assert False, 'bad operator: %s' % op

    return result

# evaluate, but give addition precedence
def evaluate2(expr):
    if isinstance(expr, int):
        return expr
    assert isinstance(expr, list), 'bad expr: %s' % expr

    result = [evaluate2(expr[0])]
    i = 1
    while i < len(expr):
        op = expr[i]
        i += 1
        assert op in ['+', '*'], 'expected operator: %s' % op

        opnd = evaluate2(expr[i])
        i += 1
        match op:
            case '+':
                result[-1] += opnd
            case '*':
                # save this operand for later
                result.append(opnd)
            case _:
                assert False, 'bad operator: %s' % op

    return math.prod(result)

def parse(numstr, i):
    expr = []
    while i < len(numstr):
        c = numstr[i]
        i += 1
        if c.isdigit():
            expr.append(int(c))
        elif c in ['+', '*']:
            expr.append(c)
        elif c == '(':
            subexpr, i = parse(numstr, i)
            expr.append(subexpr)
        elif c == ')':
            return expr, i
        else:
            assert c == ' ', 'invalid char: %s' % c
    return expr, i

def part1():
    exprs = []
    for line in readfile('day18.txt'):
        expr, i = parse(line, 0)
        assert i == len(line), 'did not parse to end of line'
        exprs.append(expr)
    print(exprs)
    print(len(exprs))

    s = 0
    for expr in exprs:
        v = evaluate(expr)
        print('eval', v)
        s += v
    print(s)

def part2():
    exprs = []
    for line in readfile('day18.txt'):
        expr, i = parse(line, 0)
        assert i == len(line), 'did not parse to end of line'
        exprs.append(expr)

    print('expr count', len(exprs))

    s = 0
    for expr in exprs:
        v = evaluate2(expr)
        print('eval', v)
        s += v
    print(s)

part2()
