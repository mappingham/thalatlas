import geopandas as gpd
import matplotlib.pyplot as plt

# load the sample GeoJSON

gdf = gpd.read_file('data/sample_seas.geojson')

print(gdf[["name", "ocean"]]) # print attribute table

# plot the seas

gdf.plot(edgecolor="black", facecolor="lightblue")
plt.title("Sample Seas")
plt.show()