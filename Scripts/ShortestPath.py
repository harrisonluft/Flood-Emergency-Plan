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

    def build_graph(self):
        itn_json = os.path.join('Materials', 'itn', 'solent_itn.json')
        with open(itn_json, 'r') as f:
            itn = json.load(f)

        self.g = nx.Graph()
        self.g.to_directed()
        road_links = itn['roadlinks']
        for link in road_links:
            wc = WeightCalculate(link, os.path.join('Materials', 'elevation', 'SZ.asc'))
            self.g.add_edge(road_links[link]['start'], road_links[link]['end'], fid=link, weight=wc.weight_start_end)
            self.g.add_edge(road_links[link]['end'], road_links[link]['start'], fid=link, weight=wc.weight_end_start)

    def get_shortest_path(self):
        shortest_path = nx.dijkstra_path(self.g, source=self.source_point, target=self.target_point, weight='weight')
        return shortest_path

















'''
path = os.chdir('/Users/linchengze/PycharmProjects/Assignment_2')


itn_json = os.path.join('Materials', 'itn', 'solent_itn.json')
with open(itn_json, 'r') as f:
    itn=json.load(f)





g = nx.Graph()
g.to_directed()
road_links = itn['roadlinks']
for link in road_links:
    wc = WeightCalculate(link, os.path.join('Materials', 'elevation', 'SZ.asc'))
    g.add_edge(road_links[link]['start'], road_links[link]['end'], fid=link, weight= wc.weight_start_end)
    g.add_edge(road_links[link]['end'], road_links[link]['start'], fid=link, weight=wc.weight_end_start)


#nx.draw(g, node_size=1)

start = 'osgb4000000026145499'
end = 'osgb4000000026142600'


shotest_path = nx.dijkstra_path(g, source=start, target=end, weight='weight')
print(shotest_path)

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