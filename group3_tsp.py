# Group: Ryan Pond, Neil Johnson, Alston Chow
# description: 
#
#

import argparse
import math
from collections import defaultdict
from datetime import datetime

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
            if city_id == "":
                cid = None
                for n in city.split(' '):
                    if n != "":
                        if not cid:
                            cid = n
                            break
                city_id = cid
            # grabbing the coordinates
            coords = city.split(' ')[-2:]
            # creating a new city object with id and coordinates
            try:
                new_city = city_obj(city_id, int(coords[0]), int(coords[1]))
            except:
                # compensating for lines with extraneous spaces
                x = None
                coords = city.split(' ')
                #del coords[0]
                for i in coords:
                    if i != "":
                        if not x:
                            x = i
                        else:
                            y = i
                new_city = city_obj(city_id, int(x), int(y))
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
            minVertex = start
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
        d = int(round(math.sqrt(x + y)))
        return d


def euler_circuit(graph):
    # Build a list where we can store the cities in
    cities = []
    temp_graph = graph

    edge_tally = defaultdict(int)

    # We will utilize Hierholzer's in a recursive fashion to assist with finding a suitable circuit.
    def create_tour(curr_city):
        # Loop through each element in the previous graph
        for e in range(len(temp_graph)):
            # If the city is equal to 0 then bypass this loop
            if temp_graph[e] == 0:
                continue
            # Otherwise if the city in question is equal to the starting point
            if curr_city == temp_graph[e][0]:
                # Modify the city set in the current location
                curr_city, connected_city = temp_graph[e]
                temp_graph[e] = 0
                create_tour(connected_city)
            elif curr_city == temp_graph[e][1]:
                connected_city, curr_city = temp_graph[e]
                temp_graph[e] = 0
                create_tour(connected_city)
        cities.insert(0, curr_city)

    # Tally up the number of edges spanning out of each city (forwards and backwards)
    for i,j in graph:
        # Add one to the first city in the set
        edge_tally[i] += 1
        # Add one to the second city in the set
        edge_tally[j] += 1

    # Set the starting value to the first city in the graph
    start = graph[0][0]

    # Loop through each city set until we find one with an odd amount of edges
    for i,j in edge_tally.items():
        if j % 2 > 0:
            # Set the starting point to the first element with an odd amount of edges
            start = i
            break

    # Set the beginning of the search to the first city set earlier
    current = start

    # Build the tour / circuit
    create_tour(current)

    # Add the first city to complete the circuit
    cities.append(cities[0])

    # Ensure that we successfully completed the circuit (first and last items are the same)
    if cities[0] != cities[-1]:
        return None

    # Return the city set that was created
    return cities

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

    #print("City Sets: ", city_sets)

    # Now find the shortest cycle between all of the cities

    # Set the starting point to spot 0
    start_vertex = mst_set[0][0]
    # Start the beginning of the circuit at 0 as well
    circuit = [city_sets[start_vertex][0]]
    # Loop through the entire MST tree until we have no more available elements to pull from
    while len(mst_set) > 0:
        #
        for i, curr_city in enumerate(circuit):
            if len(city_sets[curr_city]) > 0:
                break
        # While the total number remaining cities is above 0...
        while len(city_sets[curr_city]) > 0:
            # Save the current city number temporarily
            temp = city_sets[curr_city][0]
            # Check for duplicate connections like it
            connection_cleanup(mst_set, curr_city, temp)
            # Remove city from the set so it cannot be used again
            del city_sets[curr_city][(city_sets[curr_city].index(temp))]
            del city_sets[temp][(city_sets[temp].index(curr_city))]

            i += 1
            # Add the previously deleted city back into the circuit
            circuit.insert(i, temp)

            curr_city = temp

    return circuit


def connection_cleanup(mst_set, v1, v2):
    # This is to validate that there are no duplicate connections in our MST_SET
    for i, item in enumerate(mst_set):
        if (item[0] == v2 and item[1] == v1) or (item[0] == v1 and item[1] == v2):
            del mst_set[i]

    return mst_set

def print_list(eul_list, f_name):
    outfile = "group3_" + f_name + ".tour"
    f = open(outfile, 'w')
    ans = 0
    for i in eul_list:
        for c in t.cities:
            if str(i) == str(c.cid):
                ans += t.distance(t.cities[i], t.cities[i-1]) 

    f.write(str(int(ans))+ '\n')

    for ele in eul_list:
        f.write(str(ele) + '\n')

    f.close()

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TSP Project - Christofides Algorithm")
    parser.add_argument('filename', help="Enter the file name as 1st arg")
    arg = parser.parse_args()

    t = tsp(arg.filename)
    t.process_file()
   
    start = datetime.now().time()
    myList = t.prims(t.cities)
    updList = euler_circuit(myList)

    finish = datetime.now().time()
    t_format = "%H:%M:%S.%f"
    delta = datetime.strptime(str(finish), t_format) - datetime.strptime(str(start), t_format)
    print("Completion time: ", delta)
    #print("Path: ", *path)
    print_list(updList, arg.filename)
