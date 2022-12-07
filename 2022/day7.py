from enum import Enum
from typing import Optional

input = open('day7.txt').read().splitlines()

class Filetype(Enum):
  FILE = 1
  DIR = 2

class Node:
  type: Filetype
  size: int = 0
  totalsize: int = 0
  hasTotalsize: bool = False
  name: str = ''
  children: dict[str, 'Node']
  parent: 'Node'

  def __init__(self, name: str, type: Filetype, parent: Optional['Node']):
    self.name = name
    self.type = type
    self.children = {}
    if parent:
      self.parent = parent

  def __str__(self) -> str:
    ret = '- %s (%s' % (self.name, self.type)
    if self.type == Filetype.FILE:
      ret += ', size=%d)' % self.size
    else:
      ret += ')'
    return ret

def printNode(n: Node, indent: int = 0):
  print(' ' * indent + str(n))
  if n.type == Filetype.DIR:
    for child in n.children.values():
      printNode(child, indent + 2)

def parseCD(cwd: Node, dirname: str, root: Node) -> Node:
  if dirname == '/':
    return root
  if dirname == '..':
    return cwd.parent
  return cwd.children[dirname]

def parseLS(input: list[str], i: int, cwd: Node) -> int:
  while i < len(input) and input[i][0] != '$':
    info, name = input[i].split()
    if name not in cwd.children:
      type = Filetype.DIR if info == 'dir' else Filetype.FILE
      n = Node(name, type, cwd)
      cwd.children[name] = n
      if type != Filetype.DIR:
        n.size = int(info)
    i += 1
  return i

def parseFilesystem(input: list[str]) -> Node:
  root = Node('/', Filetype.DIR, None)
  root.parent = root
  cwd = root
  i = 1 # assume the first line is always "cd /", and we can skip it
  while i < len(input):
    tokens = input[i].split()
    assert tokens[0] == '$', 'line is not command: "%s"' % input[i]
    cmd = tokens[1]
    if cmd == 'cd':
      cwd = parseCD(cwd, tokens[2], root)
      i += 1
      continue

    if cmd == 'ls':
      i = parseLS(input, i + 1, cwd)
      continue

    assert False, 'bad input line: "%s"' % input[i]

  return root

def computeFileSizes(n: Node) -> int:
  if n.hasTotalsize:
    return n.totalsize

  if n.type == Filetype.FILE:
    n.totalsize = n.size
  else:
    n.totalsize = sum([computeFileSizes(c) for c in n.children.values()])

  n.hasTotalsize = True
  return n.totalsize

def findDirsTotalSizeAtMost(n: Node, size: int, out: list[Node]) -> None:
  if n.type == Filetype.DIR and n.totalsize <= size:
    out.append(n)
  for c in n.children.values():
    findDirsTotalSizeAtMost(c, size, out)

def findDirsAtLeast(n: Node, size: int, out: list[Node]) -> None:
  if n.type == Filetype.DIR and n.totalsize >= size:
    out.append(n)
  for c in n.children.values():
    findDirsAtLeast(c, size, out)

def part1():
  root = parseFilesystem(input)
  computeFileSizes(root)

  nodes = []
  findDirsTotalSizeAtMost(root, 100000, nodes)
  [print(n, n.totalsize) for n in nodes]
  print(sum([n.totalsize for n in nodes]))

def part2():
  root = parseFilesystem(input)
  computeFileSizes(root)

  maximum = 70000000
  unused = 30000000
  needed = maximum - root.totalsize
  assert needed < unused, 'premise of puzzle is faulty'

  nodes = []
  findDirsAtLeast(root, unused - needed, nodes)
  [print(n, n.totalsize) for n in nodes]
  print(min([n.totalsize for n in nodes]))

part2()
