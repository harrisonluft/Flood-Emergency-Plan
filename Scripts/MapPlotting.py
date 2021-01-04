import os
import json
import rasterio
from rasterio import plot
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy import crs
from shapely.geometry import LineString
import networkx as nx

class MapPlotting:

    def __init__(self, path):
        self.path = path

    def show_path(self):
        itn_json = os.path.join('Materials', 'itn', 'solent_itn.json')
        with open(itn_json, 'r') as f:
            itn = json.load(f)
        road_links = itn['roadlinks']

        g = nx.Graph()
        for link in road_links:
            g.add_edge(road_links[link]['start'], road_links[link]['end'], fid=link, weight=road_links[link]['length'])

        # nx.draw(g, node_size =1)

        wight_background = os.path.join('Materials', 'background', 'raster-50k_2724246.tif')

        links = []
        geom = []

        first_node = self.path[0]
        for node in self.path[1:]:
            link_fid = g.edges[first_node, node]['fid']
            links.append(link_fid)
            geom.append(LineString(road_links[link_fid]['coords']))
            first_node = node

        shortest_path_gpd = gpd.GeoDataFrame({'fid': links, 'geometry': geom})
        # print(shortest_path_gpd)
        # print(shortest_path_gpd.crs)
        # shortest_path_gpd.plot()

        background = rasterio.open(wight_background)
        back_array = background.read(1)
        palette = np.array([value for key, value in background.colormap(1).items()])
        background_image = palette[back_array]
        bounds = background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        display_extent = [bounds.left + 200, bounds.right - 200, bounds.bottom + 600, bounds.top - 600]

        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1, projection=crs.OSGB())

        ax.imshow(background_image, origin='upper', extent=extent, zorder=0)

        shortest_path_gpd.plot(ax=ax, edgecolor='blue', linewidth=0.5, zorder=2)

        ax.set_extent(display_extent, crs=crs.OSGB())

        plt.show()

