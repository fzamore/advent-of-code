from common.io import readfile

def addBitToEachResult(results, bit):
    for i in range(0, len(results)):
        results[i] += bit

def decodeCell(mask, cell):
    binary = list(format(cell, 'b')[::-1])
    # pad with 0's
    binary += ['0'] * (len(mask) - len(binary))
    mask = mask[::-1]

    results = ['']
    for i in range(0, len(mask)):
        m = mask[i]
        if m == '0':
            addBitToEachResult(results, binary[i])
        elif m == '1':
            addBitToEachResult(results, '1')
        elif m == 'X':
            nr = []
            for result in results:
                nr.append(result + '1')
                nr.append(result + '0')
            results = nr
        else:
            assert False, 'bad mask: %s' % mask

    return [int(x[::-1], 2) for x in results]

def decodeValue(mask, value):
    binary = list(format(value, 'b')[::-1])
    # pad with 0's
    binary += ['0'] * (len(mask) - len(binary))
    mask = mask[::-1]
    for i in range(0, len(mask)):
        m = mask[i]
        if m != 'X':
            binary[i] = m
    return int(''.join(binary[::-1]), 2)

def part1():
    mask = None
    memory = {}
    for line in readfile('day14.txt'):
        if line[0:4] == 'mask':
            mask = line.split()[2]
            continue
        assert mask != None, 'have not found mask yet'
        cell = int(line[line.find('[') + 1:line.find(']')])
        value = int(line.split()[2])
        nv = decodeValue(mask, value)
        print(cell, value, nv)
        memory[cell] = nv
    print(memory)
    print(sum(memory.values()))

def part2():
    mask = None
    memory = {}
    for line in readfile('day14.txt'):
        if line[0:4] == 'mask':
            mask = line.split()[2]
            continue
        assert mask != None, 'have not found mask yet'
        cell = int(line[line.find('[') + 1:line.find(']')])
        value = int(line.split()[2])
        for c in decodeCell(mask, cell):
            print(cell, c, value)
            memory[c] = value
    print(memory)
    print(sum(memory.values()))

part2()
