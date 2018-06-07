# Group: Ryan Pond, Neil Johnson, Alston Chow
# description: 
#
#
#

import argparse
import math
from collections import defaultdict


def addEdge(graph, u, v):
    graph[u].append(v)


# definition of function
def generate_edges(graph):
    edges = []

    # for each node in graph
    for node in graph:

        # for each neighbour node of a single node
        for neighbour in graph[node]:
            # if edge exists then append
            edges.append((int(node.cid), int(neighbour.cid)))
    return edges


class city_obj():
    """
        city class
        -> cid = city identifier
        -> priority = distances
        -> parent = parent vertex on the graph
        -> x = x coordinate
        -> y = y coordinate
        -> neighbors = list of neighboring vertices
    """

    def __init__(self, city_id, x_coord, y_coord):
        self.cid = city_id
        self.priority = 1
        self.parent = None
        self.x = x_coord
        self.y = y_coord
        self.neighbor = []


class tsp():
    """
        Travelling Salsemen Problem
        -> Utilizes Christofides algorithm
    """

    def __init__(self, t_file):
        self.data_file = open(t_file, "r")
        self.cities = []

    def process_file(self):
        """
            Description:
                -> Process the input file
                    -> Create city objects for each city
                    -> places objets in 'cities' list
        """
        for city in self.data_file:
            city = city.strip('\n')
            # grabbing the identfier
            city_id = city.split(' ')[0]
            # grabbing the coordinates
            coords = city.split(' ')[-2:]
            # creating a new city object with id and coordinates
            new_city = city_obj(city_id, int(coords[0]), int(coords[1]))
            # adding the new city to the list of cities
            self.cities.append(new_city)

    def prims(self, city_list):
        """
            Utilizes Prim's Minimal Spanning Tree Algorithm
            -> creates a graph
            Param:
                list of cities
            Returns:
                None
        """
        start = city_list[0]
        for v in city_list:
            v.priority = self.distance(v, start)
            v.parent = start
        mst = defaultdict(list)
        for i in range(len(city_list) - 1):
            minimum = 9999999999999
            minVertex = city_obj(0, 0, 0)
            for v in city_list:
                if v.priority > 0 and v.priority < minimum:
                    minimum = v.priority
                    minVertex = v
            minVertex.priority = 0
            # add edge to MST
            addEdge(mst, minVertex, minVertex.parent)
            for v in city_list:
                if v.priority > self.distance(v, minVertex):
                    v.priority = self.distance(v, minVertex)
                    v.parent = minVertex

        return generate_edges(mst)

    def distance(self, c1, c2):
        """
            Calculates the distance between 2 ciites
            Formula:
                SQRT((x2 - x1)^2 + (y2 - y1)^2)
            Param:
                c1, c2 == city objects
            Returns:
                the distance between the 2 cities
        """
        x = (c2.x - c1.x) ** 2
        y = (c2.y - c1.y) ** 2
        d = math.sqrt(x + y)
        return d


def euler_tour(mst_set):
    # Create a variable to keep track of the connected city set possibilities
    city_sets = {}
    # Go through each city pair and validate that we do not return / leave from the same city more than once
    for connection in mst_set:
        # If the city is not currently in the set, add it to it's "city number" as a blank set
        if connection[0] not in city_sets:
            city_sets[connection[0]] = []
        # Also, if the secondary city is not in the set add it as a blank set as well
        if connection[1] not in city_sets:
            city_sets[connection[1]] = []
        # Once validated, add the connected city into the previously created list sets
        city_sets[connection[0]].append(connection[1])
        city_sets[connection[1]].append(connection[0])

    print("City Sets: ", city_sets)

    # Now find the shortest cycle between all of the cities

    # Set the starting point to spot 0
    start_vertex = mst_set[0][0]
    # Start the beginning of the circuit at 0 as well
    circuit = [city_sets[start_vertex][0]]
    # Loop through the entire MST tree until we have no more available elements to pull from
    while len(mst_set) > 0:
        #
        for i, v in enumerate(circuit):
            if len(city_sets[v]) > 0:
                break
        # While the total number remaining cities is above 0...
        while len(city_sets[v]) > 0:
            # Save the current city number temporarily
            temp = city_sets[v][0]

            connection_cleanup(mst_set, v, temp)

            del city_sets[v][(city_sets[v].index(temp))]
            del city_sets[temp][(city_sets[temp].index(v))]

            i += 1
            circuit.insert(i, temp)

            v = temp

    return circuit


def connection_cleanup(mst_set, v1, v2):

    for i, item in enumerate(mst_set):
        if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
            del mst_set[i]

    return mst_set

def print_list(eul_list):
    outfile = 'tsp_output.txt'
    f = open(outfile, 'w')
    for ele in eul_list:
        f.write(str(ele) + '\n')

    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TSP Project - Christofides Algorithm")
    # parser.add_argument('filename', help="Enter the file name as 1st arg")
    # arg = parser.parse_args()

    t = tsp('tsp_example_1.txt')
    t.process_file()
    myList = t.prims(t.cities)
    print (myList)
    updList = euler_tour(myList)
    print(updList)

    current = updList[0]
    path = [current]
    visited = [False] * len(updList)

    length = 0

    for v in updList[1:]:
        if not visited[v]:
            path.append(v)
            visited[v] = True

            current = v

    path.append(path[0])

    print("Result path: ", path)

    print_list(updList)
