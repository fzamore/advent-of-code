from common.io import readfile
import math

def verify(buses, guessi, guess):
    for i in buses:
        diff = i - guessi
        if (guess + diff) % buses[i] != 0:
            return False
    return True

# Using Chinese Remainder Theorem: https://brilliant.org/wiki/chinese-remainder-theorem/
def solve(buses, i, x, m):
    x2, m2 = buses[i]
    inv = pow(m, -1, m2) # third param is modulus
    newM = m * m2
    return (m * (x2 - x) * inv + x) % newM, newM

def part1():
    time = None
    buses = []
    for line in readfile('day13.txt'):
        if time == None:
            time = int(line)
            continue
        v = line.split(',')
        for e in v:
            if e == 'x':
                continue
            buses.append(int(e))

    print(time, buses)
    d = {}
    for bus in buses:
        d[bus] = bus * math.ceil(time / bus) - time
    minBus = min(d, key=d.get)
    print(minBus * d[minBus])

def part2():
    buses = []
    for line in readfile('day13.txt'):
        if ',' not in line:
            continue
        values = line.split(',')
        for i in range(0, len(values)):
            m = values[i]
            if m == 'x':
                continue
            # convert buses into a series of equations, each with a different modulus
            # m is modulus
            m = int(m)
            # offset by negative amount
            buses.append((-i % m, m))

    print(buses)

    i = 0
    x, m = buses[i]
    while i < len(buses) - 1:
        x, m = solve(buses, i + 1, x, m)
        print(x, m)
        i += 1
    print()
    print(x)

part2()
