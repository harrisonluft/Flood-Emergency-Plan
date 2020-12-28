import json
import os
from shapely.geometry import Point
from shapely.geometry import mapping
import fiona
import networkx as nx
from rtree import index


os.chdir('C:\\Users\\17075\\Assignment_2')

# JSON file
with open(os.path.join('Materials','itn', 'solent_itn.json'), "r") as f:
    itn = json.load(f)

nodes = itn['roadnodes']
# visualizing dictionary
# print(nodes["osgb5000005195408406"]["coords"][0])


idx = index.Index()
id = 0
id_list = []
for key, value in nodes.items():
    point = Point(float(value["coords"][0]), float(value["coords"][1]))
    idx.insert(id, (point.x, point.y))
    id_list.append([key])
    id += 1

user_input = Point(450000, 85000)

for i in idx.nearest((user_input.x, user_input.y), 1):
    print(i, id_list[i])