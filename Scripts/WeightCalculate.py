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
    def __init__(self, link, path):
        self.link = link
        self.path = path

    def elevations(self):
        self.dataset = rasterio.open(self.path)
        self.elevation_raster = self.dataset.read(1)
        self.coords = []
        for coord in self.link['coords']:
            self.coords.append(round(coord[0]), round(coord[1]))
        temp_elevations = []
        for coord in self.coords:
            row, col = self.dataset.index(coord[0], coord[1])
            temp_elevations.append(self.elevation_raster[row, col])
        self.elevations = np.array(temp_elevations)
        self.array_length = self.elevations.shape

    def naismiths_height_to_time(self, start, end):
        if (end - start) > 0:
            return (end - start) * 10 / 100
        else:
            return 0

    def weight_start_end(self):
        weight = self.link['length'] * 12 / 1000
        for i in range(1, self.array_length):
            weight += self.naismiths_height_to_time(self.elevations[i-1], self.elevations[i])
        return weight

    def weight_end_start(self):
        weight = self.link['length'] * 12 / 1000
        for i in range(0, self.array_length - 1):
            weight += self.naismiths_height_to_time(self.elevations[i+1], self.elevations[i])
        return weight



