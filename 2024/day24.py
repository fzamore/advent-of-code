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

def parseInput() -> tuple[Wires, Gates, BitWires]:
  zwires: BitWires = {}
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
        zwires[outwire] = None
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

def runMachine(values: dict[str, bool], gates: Gates, z: BitWires) -> int:
  while True:
    for wire in list(values.keys()):
      for gate in gates[wire]:
        if (result := resolveGate(gate, values)) is None:
          continue

        values[gate.out] = result
        if gate.out[0] == 'z':
          z[gate.out] = result

        if (zbitstring := getBitString(z)) is not None:
          print('bitstring:', zbitstring)
          return int(zbitstring, 2)

def part1() -> None:
  values, gates, z = parseInput()
  print('data:', len(values), len(gates), len(z))

  ans = runMachine(values, gates, z)
  print(ans)

part1()
