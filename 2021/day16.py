def convertHexCharToBinaryString(hexChar):
    match hexChar:
      case '0':
        return '0000'
      case '1':
        return '0001'
      case '2':
        return '0010'
      case '3':
        return '0011'
      case '4':
        return '0100'
      case '5':
        return '0101'
      case '6':
        return '0110'
      case '7':
        return '0111'
      case '8':
        return '1000'
      case '9':
        return '1001'
      case 'A':
        return '1010'
      case 'B':
        return '1011'
      case 'C':
        return '1100'
      case 'D':
        return '1101'
      case 'E':
        return '1110'
      case 'F':
        return '1111'

    assert False, 'Invalid hex char: %s' % hexChar

def convertHexStringToBinaryString(hexString):
    result = ''
    for c in hexString:
        result += convertHexCharToBinaryString(c)
    return result

def parseVersion(bitstream, i):
    return (i + 3, int(bitstream[i:i+3], 2))

def parseTypeID(bitstream, i):
    return (i + 3, int(bitstream[i:i+3], 2))

def parseLiteral(bitstream, i):
    pos = i
    literalBitstring = ''
    while True:
        quintet = bitstream[pos:pos+5]
        literalBitstring += quintet[1:]
        pos += 5
        if quintet[0] == '0':
            break
    return (pos, int(literalBitstring, 2))

def parsePacket(bitstream, i):
    pos = i
    pos, version = parseVersion(bitstream, pos)
    pos, typeID = parseTypeID(bitstream, pos)

    literal = None
    lengthTypeID = None
    bitLimit = None
    packetLimit = None
    subPackets = []

    if typeID == 4:
        pos, literal = parseLiteral(bitstream, pos)
    else:
        lengthTypeID = bitstream[pos]
        pos += 1
        if lengthTypeID == '0':
            packetLimit = None
            bitLimit = int(bitstream[pos:pos+15], 2)
            pos += 15
            subPacketStart = pos
            while pos - subPacketStart < bitLimit:
                pos, subPacket = parsePacket(bitstream, pos)
                subPackets.append(subPacket)
        elif lengthTypeID == '1':
            packetLimit = int(bitstream[pos:pos+11], 2)
            bitLimit = None
            pos += 11
            for _ in range(packetLimit):
                pos, subPacket = parsePacket(bitstream, pos)
                subPackets.append(subPacket)
        else:
            assert False, 'Bad lengthTypeID: %s' % lengthTypeID

    packet = {
        'version': version,
        'typeID': typeID,
        'literal': literal,
        'lengthTypeID': lengthTypeID,
        'bitLimit': bitLimit,
        'packetLimit': packetLimit,
        'subPackets': subPackets,
    }

    return (pos, packet)

def getVersionSum(packet):
    result = packet['version']
    for subPacket in packet['subPackets']:
        result += getVersionSum(subPacket)
    return result

def computePacketValue(packet):
    subPackets = packet['subPackets']
    match packet['typeID']:
      case 0:
        return sum([computePacketValue(x) for x in subPackets])
      case 1:
        result = 1
        for subPacket in subPackets:
            result *= computePacketValue(subPacket)
        return result
      case 2:
        return min([computePacketValue(x) for x in subPackets])
      case 3:
        return max([computePacketValue(x) for x in subPackets])
      case 4:
        assert packet['literal'] != None, 'Missing literal in packet: %s' % packet
        return packet['literal']
      case 5:
        assert len(subPackets) == 2, 'bad subpacket count for greater than'
        return int(computePacketValue(subPackets[0]) > computePacketValue(subPackets[1]))
      case 6:
        assert len(subPackets) == 2, 'bad subpacket count for less than'
        return int(computePacketValue(subPackets[0]) < computePacketValue(subPackets[1]))
      case 7:
        assert len(subPackets) == 2, 'bad subpacket count for equal to'
        return int(computePacketValue(subPackets[0]) == computePacketValue(subPackets[1]))
      case _:
        assert False, 'Invalid typeID: %d' % packet['typeID']

def printIndent(s, indent):
    print('%s%s' % (' ' * indent, s))

def printPacket(packet, indent=0):
    printIndent('***PACKET***', indent)
    printIndent('version: %s' % packet['version'], indent)
    printIndent('typeID: %d' % packet['typeID'], indent)
    for key in ['literal', 'lengthTypeID', 'bitLimit', 'packetLimit']:
        if packet[key] != None:
            printIndent('%s: %s' % (key, packet[key]), indent)
    if len(packet['subPackets']) > 0:
        printIndent('SubPackets:', indent)
        for subPacket in packet['subPackets']:
            printPacket(subPacket, indent + 2)
    print()

def part1():
    with open('day16.txt') as f:
        lines = f.read().splitlines()
        assert len(lines) == 1, 'Expected one line in input'

        bitstream = convertHexStringToBinaryString(lines[0])
        print('bitstream length', len(bitstream))
        print()

        pos, packet = parsePacket(bitstream, 0)
        #printPacket(packet)
        print(getVersionSum(packet))

def part2():
    with open('day16.txt') as f:
        lines = f.read().splitlines()
        assert len(lines) == 1, 'Expected one line in input'

        bitstream = convertHexStringToBinaryString(lines[0])
        print('bitstream length', len(bitstream))
        print()

        pos, packet = parsePacket(bitstream, 0)
        #printPacket(packet)
        print(computePacketValue(packet))

part2()
