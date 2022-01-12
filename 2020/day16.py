from common.io import readfile
from collections import defaultdict

def isValidForRange(ranges, value, field):
    for r1, r2 in ranges[field]:
        if value >= r1 and value <= r2:
            return True
    return False

def isValidTicket(ticket, ranges):
    assert len(ranges) == len(ticket), 'mismatch ticket ranges: %s' % ticket
    for v in ticket:
        validRange = False
        for field in ranges:
            if isValidForRange(ranges, v, field):
                validRange = True
                break
        if not validRange:
            return False
    return True

def part1():
    invalidSum = 0
    ranges = []
    parsingNearby = False
    i = 0
    lines = readfile('day16.txt')
    while i < len(lines):
        line = lines[i]
        if line == '':
            i += 1
            continue

        if line == 'your ticket:':
            i += 4
            parsingNearby = True
            continue

        if not parsingNearby:
            v = line.split(':')[1].split()
            r1 = (int(v[0].split('-')[0]), int(v[0].split('-')[1]))
            r2 = (int(v[2].split('-')[0]), int(v[2].split('-')[1]))
            ranges.append(r1)
            ranges.append(r2)
        else:
            values = [int(x) for x in line.split(',')]
            for v in values:
                validRange = False
                for r1, r2 in ranges:
                    if v >= r1 and v <= r2:
                        validRange = True
                        break
                if not validRange:
                    print('invalid value', v)
                    invalidSum += v
        i += 1

    print(invalidSum)

def part2():
    ranges = {}
    myticket = []
    tickets = []
    parsingTickets = False
    i = 0
    lines = readfile('day16.txt')
    while i < len(lines):
        line = lines[i]
        if line == '':
            i += 1
            continue

        if line == 'your ticket:':
            i += 1
            myticket = [int(x) for x in lines[i].split(',')]
            i += 3
            parsingTickets = True
            continue

        if not parsingTickets:
            field = line.split(':')[0]
            v = line.split(':')[1].split()
            r1 = (int(v[0].split('-')[0]), int(v[0].split('-')[1]))
            r2 = (int(v[2].split('-')[0]), int(v[2].split('-')[1]))
            ranges[field] = (r1, r2)
        else:
            ticket = [int(x) for x in line.split(',')]
            if isValidTicket(ticket, ranges):
                tickets.append(ticket)

        i += 1

    print(ranges)
    print(tickets)
    print(myticket)

    print('fields:', len(ranges))

    potential = defaultdict(set)

    for field in ranges:
        for i in range(0, len(ticket)):
            isPotential = True
            for ticket in tickets:
                v = ticket[i]
                if not isValidForRange(ranges, v, field):
                    isPotential = False
                    break
            if isPotential:
                potential[field].add(i)

    print()
    print(potential)

    solved = {}
    while len(solved) < len(ranges):
        for field in potential:
            if len(potential[field]) == 1:
                (pos,) = potential[field]
                solved[pos] = field
                print('single pos', field, pos)
                for field in potential:
                    if pos in potential[field]:
                        potential[field].remove(pos)

    print(solved)

    prod = 1
    for pos in solved:
        field = solved[pos]
        if field[0:9] == 'departure':
            print('departure field', pos)
            prod *= myticket[pos]
    print(prod)

part2()
