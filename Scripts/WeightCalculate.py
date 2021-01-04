import networkx as nx
import os
import json
import rasterio
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy import crs
from shapely.geometry import LineString



#formulate Naismith's Rule in: 12 min / 1 km + 10 min / 100 m

class WeightCalculate:
    def __init__(self, link):
        self.link = link

    def weight_start_end(self):
        weight = self.link['length'] * 12 / 1000
        elevations = []
        for coord in self.link['coords']:
            elevations.add()





    def weight_end_start(self):