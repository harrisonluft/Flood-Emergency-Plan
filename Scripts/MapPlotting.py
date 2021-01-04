import os
import json
import rasterio
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy import crs
from shapely.geometry import LineString
import networkx as nx


os.chdir('/Users/linchengze/PycharmProjects/Assignment_2')

path = ['osgb4000000026219230', 'osgb4000000026142373', 'osgb4000000026227672', 'osgb4000000026142366', 'osgb4000000026142357', 'osgb4000000026142355', 'osgb4000000026142354', 'osgb4000000026142353', 'osgb4000000026142362', 'osgb4000000026142302', 'osgb4000000026142304', 'osgb4000000026142305', 'osgb4000000026142306', 'osgb4000000026142301', 'osgb4000000026142315', 'osgb4000000026142323', 'osgb4000000026142317', 'osgb4000000026142474', 'osgb4000000026142428', 'osgb4000000026226895', 'osgb4000000026142430', 'osgb4000000026142429', 'osgb4000000026142437', 'osgb4000000026142438', 'osgb4000000026142434', 'osgb4000000026142435', 'osgb4000000026142436', 'osgb4000000026142468', 'osgb4000000026142497', 'osgb4000000026142498', 'osgb4000000026242058', 'osgb4000000026221467', 'osgb5000005190446083']



itn_json = os.path.join('Materials', 'itn', 'solent_itn.json')
with open(itn_json, 'r') as f:
    itn = json.load(f)
road_links = itn['roadlinks']

g = nx.Graph()
for link in road_links:
    g.add_edge(road_links[link]['start'], road_links[link]['end'], fid = link, weight = road_links[link]['length'])

#nx.draw(g, node_size =1)

wight_background = os.path.join('Materials', 'background', 'raster-50k_2724246.tif')

links = [] # this list will be used to populate the feature id (fid) column
geom  = [] # this list will be used to populate the geometry column

first_node = path[0]
for node in path[1:]:
    link_fid = g.edges[first_node, node]['fid']
    links.append(link_fid)
    geom.append(LineString(road_links[link_fid]['coords']))
    first_node = node

shortest_path_gpd = gpd.GeoDataFrame({'fid': links, 'geometry': geom})
print(shortest_path_gpd)
shortest_path_gpd.plot()

background = rasterio.open(wight_background)
back_array = background.read(1)
palette = np.array([value for key, value in background.colormap(1).items()])
background_image = palette[back_array]
bounds = background.bounds
extent = [bounds.left, bounds.right, bounds.bottom,  bounds.top]
display_extent = [bounds.left+200, bounds.right-200, bounds.bottom+600, bounds.top-600]

fig = plt.figure(figsize=(3,3), dpi=300)
ax = fig.add_subplot(1,1,1, projection=crs.epsg(27700))

ax.imshow(background_image, origin='upper', extent=extent, zorder=0)

shortest_path_gpd.plot(ax=ax, edgecolor='blue', linewidth=0.5, zorder=2)

ax.set_extent(display_extent, crs=crs.epsg(27700))