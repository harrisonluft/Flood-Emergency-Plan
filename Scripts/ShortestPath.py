import networkx as nx
import os
import json
import rasterio
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy import crs
from shapely.geometry import LineString
from WeightCalculate import WeightCalculate




class ShortestPath:

    def __init__(self, source_point, target_point):

        self.source_point = source_point
        self.target_point = target_point

    def get_itn_and_elevation(self):
        self.itn_json = os.path.join('Materials', 'itn', 'solent_itn.json')
        with open(self.itn_json, 'r') as f:
            self.itn = json.load(f)

        self.dataset = rasterio.open(os.path.join('Materials', 'elevation', 'SZ.asc'))
        self.elevation_raster = self.dataset.read(1)

    def weight_calculate(self, length, coords):
        temp_coords = []
        for coord in coords:
            temp_coords.append([round(coord[0]), round(coord[1])])
        temp_elevations = []
        for coord in temp_coords:
            row, col = self.dataset.index(coord[0], coord[1])
            temp_elevations.append(self.elevation_raster[row, col])
        elevations = np.array(temp_elevations)
        array_length = elevations.shape

        weight_start_end = length * 12 / 1000
        for i in range(1, array_length[0]):
            x = elevations[i] - elevations[i - 1]
            if x > 0:
                weight_start_end += x * 10 / 100

        weight_end_start = length * 12 / 1000
        for i in range(0, array_length[0] - 1):
            x = elevations[i] - elevations[i + 1]
            if x > 0:
                weight_end_start += x * 10 / 100

        return weight_start_end, weight_end_start


    def create_graph(self):
        self.g = nx.DiGraph()
        road_links = self.itn['roadlinks']
        for link in road_links:
            weight = self.weight_calculate(road_links[link]['length'], road_links[link]['coords'])
            weight1 = weight[0]
            weight2 = weight[1]
            self.g.add_edge(road_links[link]['start'], road_links[link]['end'], fid=link, weight=weight1)
            self.g.add_edge(road_links[link]['end'], road_links[link]['start'], fid=link, weight=weight2)



    def get_shortest_path(self):
        shortest_path = nx.dijkstra_path(self.g, source=str(self.source_point), target=str(self.target_point), weight='weight')
        shortest_path_time = nx.shortest_path_length(self.g, source=str(self.source_point), target=str(self.target_point), weight='weight')


        return shortest_path, shortest_path_time


















'''


path = os.chdir('/Users/linchengze/PycharmProjects/Assignment_2')


itn_json = os.path.join('Materials', 'itn', 'solent_itn.json')
with open(itn_json, 'r') as f:
    itn=json.load(f)

dataset = rasterio.open(os.path.join('Materials', 'elevation', 'SZ.asc'))
elevation_raster = dataset.read(1)

def weight_calculate(length, coords):
    temp_coords = []
    for coord in coords:
        temp_coords.append([round(coord[0]), round(coord[1])])
    temp_elevations = []
    for coord in temp_coords:
        row, col = dataset.index(coord[0], coord[1])
        temp_elevations.append(elevation_raster[row, col])
    elevations = np.array(temp_elevations)
    array_length = elevations.shape

    weight = length * 12 / 1000
    for i in range(1, array_length[0]):
        x = elevations[i] - elevations[i-1]
        if x > 0:
            weight += x * 10 / 100
    return weight

def weight_calculate_desc(length, coords):
    temp_coords = []
    for coord in coords:
        temp_coords.append([round(coord[0]), round(coord[1])])
    temp_elevations = []
    for coord in temp_coords:
        row, col = dataset.index(coord[0], coord[1])
        temp_elevations.append(elevation_raster[row, col])
    elevations = np.array(temp_elevations)
    array_length = elevations.shape

    weight = length * 12 / 1000
    for i in range(0, array_length[0]-1):
        x = elevations[i] - elevations[i+1]
        if x > 0:
            weight += x * 10 / 100
    return weight

g = nx.DiGraph()
road_links = itn['roadlinks']
for link in road_links:
    weight1 = weight_calculate(road_links[link]['length'], road_links[link]['coords'])
    weight2 = weight_calculate_desc(road_links[link]['length'], road_links[link]['coords'])
    if weight1 != weight2:
        print(weight1, weight2)
    g.add_edge(road_links[link]['start'], road_links[link]['end'], fid=link, weight = weight1)
    g.add_edge(road_links[link]['end'], road_links[link]['start'], fid=link, weight = weight2)
g.to_directed()
#print(g.edges)
#nx.draw(g, node_size=1)



g2 = nx.Graph()
g2.to_directed()
road_links = itn['roadlinks']
for link in road_links:
    g2.add_edge(road_links[link]['end'], road_links[link]['start'], fid=link,
                weight = road_links[link]['length']*12/1000)



start = 'osgb4000000026145499'
end = 'osgb4000000026142600'


shotest_path = nx.dijkstra_path(g, source=start, target=end, weight='weight')
shortest_path_length = nx.shortest_path_length(g, source=start, target=end, weight='weight')
print(shotest_path)
print(shortest_path_length)

shotest_path2 = nx.dijkstra_path(g2, source=start, target=end, weight='weight')
shortest_path_length2 = nx.shortest_path_length(g2, source=start, target=end, weight='weight')
print(shotest_path2)
print(shortest_path_length2)


wight_background = os.path.join('Materials', 'background', 'raster-50k_2724246.tif')

links = [] # this list will be used to populate the feature id (fid) column
geom  = [] # this list will be used to populate the geometry column

first_node = shotest_path[0]
for node in shotest_path[1:]:
    link_fid = g.edges[first_node, node]['fid']
    links.append(link_fid)
    geom.append(LineString(road_links[link_fid]['coords']))
    first_node = node

shortest_path_gpd = gpd.GeoDataFrame({'fid': links, 'geometry': geom})

shortest_path_gpd.plot()
'''