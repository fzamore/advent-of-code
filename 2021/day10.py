import math

def isOpeningToken(token):
    match token:
      case '(':
        return True
      case '[':
        return True
      case '{':
        return True
      case '<':
        return True

    return False

def isClosingToken(token):
    match token:
      case ')':
        return True
      case ']':
        return True
      case '}':
        return True
      case '>':
        return True

    return False

def getClosingToken(openingToken):
    assert isOpeningToken(openingToken), 'Bad token input in getClosingToken: %s' % openingToken
    matches = {'(': ')', '[': ']', '{': '}', '<': '>'}
    return matches[openingToken]

def isTokenMatch(opening, closing):
    matches = ['()', '[]', '{}', '<>']
    for match in matches:
        if match[0] == opening and match[1] == closing:
            return True
    return False

def getTokenScore(token):
    match token:
      case ')':
        return 3
      case ']':
        return 57
      case '}':
        return 1197
      case '>':
        return 25137

    print('Bad getTokenScore input', token)
    assert False

def getTokenScore2(token):
    match token:
      case ')':
        return 1
      case ']':
        return 2
      case '}':
        return 3
      case '>':
        return 4

    print('Bad getTokenScore2 input', token)
    assert False

def part1():
    f = open('day10.txt')
    total = 0
    stack = []
    for line in f.readlines():
        for token in line[:-1]:
            if isOpeningToken(token):
                stack.append(token)
            elif isClosingToken(token):
                if isTokenMatch(stack[-1], token):
                    stack.pop()
                else:
                    total += getTokenScore(token)
                    break
            else:
                print('Bad line:', token, line)

    print(total)

    f.close()

def part2():
    f = open('day10.txt')
    scores = []
    for line in f.readlines():
        score = 0
        stack = []
        corruptLine = False
        for token in line[:-1]:
            if isOpeningToken(token):
                stack.append(token)
            elif isClosingToken(token):
                if isTokenMatch(stack[-1], token):
                    stack.pop()
                else:
                    corruptLine = True
                    break
            else:
                print('Bad line:', token, line)

        if corruptLine:
            continue

        stack.reverse()
        for token in stack:
            assert isOpeningToken(token), 'Invalid token found in stack: %s' % token
            closingToken = getClosingToken(token)
            score *= 5
            score += getTokenScore2(closingToken)

        scores.append(score)

    print(sorted(scores)[math.floor(len(scores) / 2)])

    f.close()

part2()
