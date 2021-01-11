import networkx as nx
import os
import json
import rasterio
import numpy as np


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

