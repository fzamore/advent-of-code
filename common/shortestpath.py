from collections import defaultdict
from collections.abc import Hashable
from heapq import heappush, heappop

# Implementation of Dijkstra's shortest-path algorithm.
# Params:
#  startNode (hashable): start node. distance to this node will always be zero
#  getAdjacentNodes (node => list of (node, distance) tuples): nodes adjacent to given node
#  isDestNode (node => Boolean): whether this node is a destination, and the algorithm can terminate
# Return value:
#  (node, distance) tuple for destination node and distance to that node
def dijkstra(startNode, getAdjacentNodes, isDestNode):

    # min-heap priority queue of points with distance from start as the key
    q = []

    # map from point to distance from start
    d = defaultdict(lambda: float('inf'))

    # initialize with the start point
    heappush(q, (0, startNode))
    d[startNode] = 0

    while len(q) > 0:
        node = heappop(q)[1]
        nodeDist = d[node]
        assert nodeDist != float('inf'), 'Missing point in dict for node: %s' % str(node)

        if isDestNode(node):
            # done
            return (node, nodeDist)

        for adjNode, adjNodeDist in getAdjacentNodes(node):
            newDist = nodeDist + adjNodeDist
            if newDist < d[adjNode]:
                # We've improved the distance to this point. Update the queue
                # and distance map. We don't need to modify its existing entry
                # in the priority queue (if it exists) because the new entry
                # will always be lower, and thus will be popped off the queue
                # before the existing entry.
                d[adjNode] = newDist
                heappush(q, (newDist, adjNode))

    assert False, 'did not find shortest path'
