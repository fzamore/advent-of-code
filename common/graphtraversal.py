from collections import deque
from typing import Any, Callable, Collection, Hashable, Iterable, Optional, TypeVar

T = TypeVar('T', bound=Hashable)

# Implementation of a BFS algorithm that visits each node in BFS order.
# Params:
#  startNode (hashable): start node
#  getAdjacentNodes (node => list of nodes): nodes adjacent to given node
#  visitNode (optional) ((node, numSteps) => bool): visits the given node, including
#       the number of steps it took to get to it. Returns true if the algorithm
#       should continue past this node, or false if this branch is a dead-end.
# isEndNode (optional) (node => bool): returns whether the given node
#       is an "end node". If this function returns true, the
#       algorithm will stop and not process any additional nodes.
# Return value:
#   dict[node, distance] containing the number of hops to each reachable node
def bfs(
  startNode: T,
  getAdjacentNodes: Callable[[T], Iterable[T]],
  visitNode: Optional[Callable[[T, int], bool]] = None,
  isEndNode: Optional[Callable[[T], bool]] = None,
) -> dict[T, int]:
  seen: set[T] = {startNode}
  q: deque[tuple[int, T]] = deque()
  q.append((0, startNode))
  result: dict[T, int] = {}

  while len(q) > 0:
    numSteps, node = q.popleft()
    assert node not in result, 'already seen node'
    result[node] = numSteps
    if visitNode is not None and not visitNode(node, numSteps):
      # Skip this node if its visitation function returned false.
      continue

    if isEndNode is not None and isEndNode(node):
      # We've reached an end node. Stop.
      return result

    for adjNode in getAdjacentNodes(node):
      if adjNode in seen:
        continue
      seen.add(adjNode)

      # Keep going.
      q.append((numSteps + 1, adjNode))

  return result

# Implementation of a DFS algorithm that visits each node.
# Params:
#   startNode (hashable): start node
#   getAdjacentNodes (node => list of nodes): nodes adjacent
#       to given node.
#   seenNode (optional): set of previously-seen nodes
#   visitNode (optional) ((node) => None): visits the given node
# Return value:
#   None
def dfs(
  startNode: T,
  getAdjacentNodes: Callable[[T], Iterable[T]],
  seenNodes: set[T] = set(),
  visitNode: Optional[Callable[[T], None]] = None,
) -> None:
  if startNode in seenNodes:
    return
  seenNodes.add(startNode)
  if visitNode is not None:
    visitNode(startNode)

  for adjNode in getAdjacentNodes(startNode):
    dfs(adjNode, getAdjacentNodes, seenNodes, visitNode)

# Returns a list of all connected components of a given graph.
# Params:
#   allNodes: list of nodes in the graph (arbitrarily ordered)
#   getAdjacentNodes (node => list of nodes): nodes adjacent
#       to given node.
# Return value:
#   list of connected components (each connected component is
#   itself a list of nodes)
def getConnectedComponents(
  allNodes: Iterable[T],
  getAdjacentNodes: Callable[[T], Iterable[T]],
) -> Collection[Collection[T]]:
  result: list[Collection[T]] = []
  remainingNodes = set(allNodes)
  while len(remainingNodes) > 0:
    # Choose an arbitrary start node.
    for startNode in remainingNodes: break

    # Run a DFS from this node.
    seenNodes: set[T] = set()
    dfs(startNode, getAdjacentNodes, seenNodes)

    # Remove all seen nodes from the set of remaining nodes.
    remainingNodes.difference_update(seenNodes)
    result.append(list(seenNodes))

  return result
