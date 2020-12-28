import json
from shapely.geometry import Point
from rtree import index


class Itn:

    def __init__(self, itn_path):
        self.itn_path = itn_path

    def itn_index(self):

        # JSON file
        with open(self.itn_path, "r") as self.f:
            self.itn = json.load(self.f)

        self.nodes = self.itn['roadnodes']

        self.idx = index.Index()
        self.id = 0
        self.id_list = []
        for key, value in self.nodes.items():
            self.point = Point(float(value["coords"][0]), float(value["coords"][1]))
            self.idx.insert(self.id, (self.point.x, self.point.y))
            self.id_list.append([key])
            self.id += 1

    def nearest_node(self, user_input):

        for i in self.idx.nearest((user_input.x, user_input.y), 1):
            return print(i, self.id_list[i])
