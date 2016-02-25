import json
import sys
from pprint import pprint
import heapq
import Queue

'''
This file is designed to find the bridge nodes on the undirected graph.
We will use Tarjan's linear-time algorithm to find the bridges of 
a graph.

I assume that the higher the degree of a bridge vertex, the more we want
that vertex to be a part of our initial seeding.
'''

# From just a list of edges, we will create the appropriate adjacencyList.
# Note: This graph is undirected, and we do not care about 0 degree nodes.
def createAdjList(edges):
    adjList = {}

    # Recall, edges are in tuple form. Each node is still in string form.
    for edge in edges:
        srcNode = edge[0]
        destNode = edge[1]

        # Since this is we want this to be directed (for bridge detection)
        if srcNode in adjList:
            adjList[srcNode].append(destNode)

        else:
            adjList[srcNode] = [destNode]

    return adjList

# This will output an adjacencyList to a JSON file. This is just to check
# the legitimacy of an adjacency list.
def listToJSON(adjacencyList):
    jsonString = json.dumps(adjacencyList)
    outFile = open("adjList", "w")
    outFile.write(jsonString)

# Like the name suggests, this simply just finds the minimum spanning tree
# of the graph.
def findMinSpanTrees(adjacencyList):
    # Since we don't really have any weights associated with each of
    # the edges, this algorithm is basically DFS. 
    # We take the first node in the adjacency list to be our start.

    # Edges will contain tuples, representing edges
    edges = []

    # Vertices will contain just string values of the node.
    vertices = []

    # In case the graph is disconnected, we will find several trees.
    treesAdjList = []
    treeEdges = []

    # We want the total number of vertices.
    numVertices = len(adjacencyList.keys())

    # Stack for DFS
    stack = []

    stack.append("DONE")

    # Start Index in case for disconnected nodes.
    startIdx = 0

    # We just operating on the first node.
    startNode = adjacencyList.keys()[startIdx]
    neighbors = adjacencyList[startNode]
    vertices.append(startNode)

    # We go until we find the first vertex with neighbors
    # That is, we go until we find our first connected component.
    while neighbors[0] == "" and startIdx < numVertices - 1:
        startIdx += 1
        startNode = adjacencyList.keys()[startIdx]
        neighbors = adjacencyList[startNode]
        vertices.append(startNode)

    # Once we hit a connected component, we start populating DAT QUEUE.
    for neighbor in neighbors:
        edge = (startNode, neighbor)

        # The moment we can move, we stop the for loop.
        if neighbor not in vertices:
            currEdge = edge
            vertices.append(neighbor)
            edges.append(edge)
            break

    while len(vertices) != numVertices:
        # Two cases here:
        # 1: The stack is now empty (we exhausted this component)
        #       We first make an adjacency matrix for this.
        #       In this case, we keep incrementing startIdx until
        #       we encounter an unvisited connected component.
        #
        # 2: The stack is not empty
        #       In this case, we just keep going through that component.
        if currEdge == "DONE":
            # First, adding the new edges and the adjacency matrix into
            # the appropriate lists.
            treeEdges.append(edges)
            adjList = createAdjList(edges)
            treesAdjList.append(adjList)

            # Next, resetting the edge vector.
            edges = []

            # Now, we find the next connected component.
            if startIdx < numVertices - 1:
                startIdx += 1
                startNode = adjacencyList.keys()[startIdx]
                neighbors = adjacencyList[startNode]

                if startNode not in vertices:
                    vertices.append(startNode)  

            # We go until we find a vertex with neighbors
            # That is, we go until we find our connected component.
            while (neighbors[0] == "" or startNode in vertices) and \
                  startIdx < numVertices - 1:
                startIdx += 1
                startNode = adjacencyList.keys()[startIdx]
                neighbors = adjacencyList[startNode]

                if startNode not in vertices:
                    vertices.append(startNode)  

            # Once we hit a connected component, we start populating DAT QUEUE.
            for neighbor in neighbors:
                edge = (startNode, neighbor)
                if neighbor not in vertices:
                    stack.append("DONE")
                    currEdge = edge
                    vertices.append(neighbor)
                    edges.append(edge)
                    break

        # Occurs if there already is stuff inside the Queue.
        else:
            srcNode = currEdge[0]
            destNode = currEdge[1]

            # Both nodes should technically be inside the array.
            nextNeighbors = adjacencyList[destNode]
            # There should always be neighbors in this case.
            unVisitedNeighbor = False

            for neighbor in nextNeighbors:
                edge = (destNode, neighbor)
                if neighbor not in vertices:
                    stack.append(currEdge)
                    currEdge = edge
                    vertices.append(neighbor)
                    edges.append(edge)
                    unVisitedNeighbor = True
                    break

            if unVisitedNeighbor == False:
                currEdge = stack.pop()

    # This is for the last connected component.
    treeEdges.append(edges)
    adjList = createAdjList(edges)
    treesAdjList.append(adjList)

    return (treeEdges, treesAdjList)

# Ordering the vertices so that we can do the bridge algorithm well.
def preOrderVertices(edges, numVertices):
    # Since the edges are preordered, we just go through the edges.

    # Just to ensure that we got all the vertices.
    vertices = []

    # Return value. This list will hold tuples; first index holding the 
    # order of the vertex. Second index holding the id of the node.
    orderedVertices = []

    # Starting order:
    orderIdx = 1

    # Starting with the root node.
    rootEdge = edges[0]
    rootVert = rootEdge[0]

    # Creating the tuple
    orderedVertex = (orderIdx, rootVert)

    # Adding it to the lists so we can keep track of the met vertices.
    vertices.append(rootVert)
    orderedVertices.append(orderedVertex)

    for edge in edges:
        continue





# Using minimum spanning trees, we will be finding the bridge vertices.
# This uses Tarjan's algorithm.
def findBridges(adjacencyList):
    # Getting the the total number of vertices:
    numVertices = len(adjacencyList.keys())

    # First, we need to find the minimum spanning trees
    spanEdges, spanTrees = findMinSpanTrees(adjacencyList)
    listToJSON(spanTrees[0])
    # Now, we iterate through the edges in pre-order, which
    # is basically what it is right now. (thanks DFS :))
    


def ND(node, adjacencyList):
    pass
# This basically parses the stuff and then invokes the bridge.
def run(rounds = 50):
    # This is the JSON file that will be parsed.
    JSONfile = sys.argv[1]

    # Recall that the JSON file is in the form:
    # num_players.num_seeds.uniqueID
    JSONinfo = JSONfile.split('.')
    numPlayers = int(JSONinfo[0])
    numSeeds = int(JSONinfo[1])
    uniqueID = int(JSONinfo[2])

    with open(JSONfile) as dataFile:
        JSONdata = json.load(dataFile)

    # Storing the top nodes for optimal choices.
    topNodes = []

    # Storing the adjacency matrix of the entire thing.
    adjacencyList = {}

    # Populating this beautiful dictionary.
    for key, val in JSONdata.iteritems():
        adjacencyList[key] = val

    bridgeNodes = findBridges(adjacencyList)

if __name__ == '__main__':

    # If the number of arguments isn't correct, we print a usage thing.
    if len(sys.argv) < 2:
        print "Usage: python", sys.argv[0], "GRAPH.json [ITERATIONS]\n" \
              "Example: python", sys.argv[0], "2.5.1.json"
        sys.exit()

    if len(sys.argv) == 3:
        rounds = int(sys.argv[2])
        run(rounds = rounds)
    else:
        run()