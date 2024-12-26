from collections import namedtuple, defaultdict
from enum import Enum
from typing import Optional

input = open('day24.txt').read().splitlines()

class GateType(Enum):
  AND = 1
  OR = 2
  XOR = 3

Gate = namedtuple('Gate', ['type', 'in1', 'in2', 'out'])

# Representation of a collection of wires that represent a binary value.
BitWires = dict[str, Optional[bool]]

# Mapping of wire -> list of gates that has that wire as an input.
Gates = dict[str, list[Gate]]

Wires = dict[str, bool]

def parseInput() -> tuple[Wires, Gates, list[str]]:
  zwires = []
  gates = defaultdict(list)
  values = {}
  for line in input:
    if line == '':
      continue

    if ':' in line:
      w, v = line.split(': ')
      values[w] = v == '1'
      assert w[0] != 'z', 'z-wire should not have initial value'
    else:
      assert '>' in line, 'bad line'
      inwires, outwire = line.split(' -> ')
      in1, gateTypeStr, in2 = inwires.split()
      assert in1[0] != 'z' and in2[0] != 'z', 'input wires should not be z-wires'
      assert outwire[0] not in ['x', 'y'], 'output wires should not be x- or y-wires'
      if outwire[0] == 'z':
        zwires.append(outwire)
      gateType = [g for g in GateType if g.name == gateTypeStr][0]
      gate = Gate(gateType, in1, in2, outwire)
      gates[in1].append(gate)
      gates[in2].append(gate)

  return values, gates, zwires

# Returns a bitstring if the entire input is populated; none otherwise.
def getBitString(bitWires: BitWires) -> Optional[str]:
  if None in bitWires.values():
    return None

  b = ['1' if bitWires[k] else '0' for k in sorted(bitWires.keys(), reverse=True)]
  return ''.join(b)

def resolveGate(gate: Gate, values: dict[str, bool]) -> Optional[bool]:
  in1v, in2v = values.get(gate.in1), values.get(gate.in2)
  if in1v is None or in2v is None:
    return None

  match gate.type:
    case GateType.AND:
      return in1v and in2v
    case GateType.OR:
      return in1v or in2v
    case GateType.XOR:
      return in1v ^ in2v
    case _:
      assert False, 'bad gate type'

def runMachine(values: dict[str, bool], gates: Gates, zwires: list[str]) -> int:
  zbitwires: BitWires = dict((k, None) for k in zwires)
  while True:
    for wire in list(values.keys()):
      for gate in gates[wire]:
        if (result := resolveGate(gate, values)) is None:
          continue

        values[gate.out] = result
        if gate.out[0] == 'z':
          zbitwires[gate.out] = result

        if (zbitstring := getBitString(zbitwires)) is not None:
          print('bitstring:', zbitstring)
          return int(zbitstring, 2)

# Returns a gate matching the given gate type and input wire.
def findGate(gates: Gates, type: GateType, inputWire: str) -> Optional[Gate]:
  result = None
  for gatelist in gates.values():
    for gate in gatelist:
      if gate.type == type and inputWire in [gate.in1, gate.in2]:
        assert result is None or result == gate, 'duplicate gate found'
        result = gate

  return result

def part1() -> None:
  values, gates, zwires = parseInput()
  print('data:', len(values), len(gates), len(zwires))

  ans = runMachine(values, gates, zwires)
  print(ans)

def part2() -> None:
  values, gates, zwires = parseInput()
  print('data:', len(values), len(gates), len(zwires))

  # Binary addition via AND, OR, and XOR gates is performed as follows.
  # x_i and y_i are input bits, c is the carry bit (initially set to 0),
  # and z_i is the output bit.
  #
  #   (x_i XOR y_i) XOR c => z_i
  #   (x_i AND y_i) OR ((x_i XOR y_i) AND c) => c
  #
  # To reduce this to a "flat" list of gates where each input is only a
  # single bit (as opposed to an expression), we introduce "temporary"
  # bits/wires as p, q, and r:
  #
  #   x_i XOR y_i => p
  #   x_i AND y_i => q
  #   p AND c => r
  #   c XOR p => z_i
  #   q OR r => c
  #
  # This implies that for each bit, we need five gates. We look through
  # our list of gates and find those that don't match this pattern
  # (going bit by bit).

  # Create a mapping from wire to gate whose output is that wire.
  outgates = {}
  for wire in gates:
    for gate in gates[wire]:
      outgates[gate.out] = gate

  swaps = []
  # We assume that wires for bits 00 and 45 are correctly formed (verified
  # by experimentation).
  for i in range(1, 45):
    code = str(i).zfill(2)

    xwire = 'x' + code
    ywire = 'y' + code
    zwire = 'z' + code

    xyXorGate = findGate(gates, GateType.XOR, xwire)
    assert xyXorGate is not None, 'did not find xy XOR gate'
    assert ywire in [xyXorGate.in1, xyXorGate.in2], 'xy XOR gate did not have x and y as inputs'

    xyAndGate = findGate(gates, GateType.AND, xwire)
    assert xyAndGate is not None, 'did not find xy AND gate'
    assert ywire in [xyAndGate.in1, xyAndGate.in2], 'xy AND gate did not have x and y as inputs'

    # x_i XOR y_i => p
    pwire = xyXorGate.out

    # p AND c => r
    rgate = findGate(gates, GateType.AND, pwire)
    if rgate is None:
      # There is no r gate whose type is AND.
      qwire = xyAndGate.out

      # q OR r => c
      cgate = findGate(gates, GateType.OR, qwire)
      assert cgate is None, 'c gate should also be messed up if r gate is messed up'

      # Swap the pwire and qwire. This may not work in the general case,
      # but it works for my input.
      print('r gate problem:', i, pwire, qwire)
      swaps.append((pwire, qwire))

    # p XOR c => z_i
    zgate = findGate(gates, GateType.XOR, pwire)
    if zgate is not None and zgate != outgates[zwire]:
      # The z gate's output is not correctly set (i.e., it's not to a
      # z-wire). Make a swap so that the z-gate has an output of the
      # z-wire.
      assert zgate.out[0] != 'z', 'z gate should have had mismatch'
      print('z gate mismatch:', i, zgate.out, outgates[zwire].out)
      swaps.append((zgate.out, outgates[zwire].out))

  print('swaps:', len(swaps), swaps)
  ans = ','.join(sorted(sum(swaps, ())))
  print(ans)

part2()
