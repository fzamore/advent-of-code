from collections import deque
from typing import Any, Callable,Hashable, Iterable, Optional, TypeVar

T = TypeVar('T', bound=Hashable)

# Implementation of a BFS algorithm that visits each node in BFS order.
# Params:
#  startNode (hashable): start node
#  getAdjacentNodes (node => list of (node, extraData) tuples): nodes adjacent
#       to given node. extraData can be anything, but must be supplied (use None
#       if not needed).
#  visitNode ((node, extraData) => bool): visits the given node (along with
#       optional extraData). Returns true if the algorithm should continue past
#       this node, or false if this branch is a dead-end.
#  isEndNode (optional) ((node, extraData) => bool): returns whether the given node
#       (and optional extraData) is an "end node". If this function returns true, the
#       algorithm will stop and not process any additional nodes.
# Return value:
#  dict[node, distance] containing the number of hops to each reachable node
def bfs(
  startNode: T,
  getAdjacentNodes: Callable[[T], Iterable[tuple[T, Any]]],
  visitNode: Callable[[T, Optional[Any]], bool],
  isEndNode: Optional[Callable[[T, Optional[Any]], bool]] = None,
) -> dict[T, int]:
  seen: set[T] = {startNode}
  q: deque[tuple[int, T]] = deque()
  q.append((0, startNode))
  result: dict[T, int] = {}

  while len(q) > 0:
    numSteps, node = q.popleft()
    assert node not in result, 'already seen node'
    result[node] = numSteps
    for adjNode, extraData in getAdjacentNodes(node):
      if adjNode in seen:
        continue
      seen.add(adjNode)

      if visitNode(adjNode, extraData):
        if isEndNode is not None and isEndNode(adjNode, extraData):
          # We reached an end node. Add an entry to the result and stop.
          result[adjNode] = numSteps + 1
          return result
        q.append((numSteps + 1, adjNode))

  return result
