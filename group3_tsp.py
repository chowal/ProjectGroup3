# Group: Ryan Pond, Neil Johnson, Alston Chow
# description: 
#
#
#

import argparse
import math

class city_obj():
    """
        city class
        -> cid = city identifier
        -> priority = distances
        -> parent = parent vertex on the graph
        -> x = x coordinate
        -> y = y coordinate
        -> neighbors = list of neighoring vertices
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
            city_id  = city.split(' ')[0]
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
        MST = []
        for i in range(len(city_list)):
            minimum = 9999999999999
            minVertex = city_obj(0,0,0)
            for v in city_list:
                if v.priority > 0 and v.priority < minimum:
                    minimum = v.priority
                    minVertex = v
            minVertex.priority = 0
            # add edge to MST
            #MST.append(
            for v in city_list:
                if v.priority > self.distance(v, minVertex):
                    v.priority = self.distance(v, minVertex)
                    v.parent = minVertex
        

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
        x = (c2.x - c1.x)**2
        y = (c2.y - c1.y)**2
        d = math.sqrt(x + y)
        return d
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= "TSP Project - Christofides Algorithm")
    parser.add_argument('filename', help="Enter the file name as 1st arg")
    arg = parser.parse_args()

    
    t = tsp(arg.filename)
    t.process_file()
    t.prims(t.cities)
