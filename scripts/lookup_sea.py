# Thalatlas Sea Lookup

    # loads metadata from sample_hierarchy.json
    # loads polygons from sample_seas.geojson
    # asks for partial sea name (e.g. 'carib' for Caribbean Sea)
    # finds first metadata match and prints details
    # finds matching polygons and plots them

import json
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt

# paths to data files

DATA_JSON = Path("data/sample_hierarchy.json") # metadata for oceans/seas/subseas
GEOJSON_FILE = Path("data/sample_seas.geojson") # polygons for seas

# load JSON hierarchy metadata

if DATA_JSON.exists():
    with open(DATA_JSON, "r") as f:
        hierarchy = json.load(f)
else:
    print(" sample_hierarchy.json not found")
    hierarchy = {}

# load GeoJSON polygons into GeoPandas GeoDataFrame

if GEOJSON_FILE.exists():
    gdf = gpd.read_file(GEOJSON_FILE)

else:
    print(" sample_seas.geojson not found")

    # create empty GeoDataFrame with same columns

    gdf = gpd.GeoDataFrame(columns=["name","ocean", "geometry"])

# helper: find sea metadata (name, ocean, alt names, notes) from JSON

def find_sea_metadata(sea_input):
    # normalize input (lowercase, strip spaces)
    sea_input = sea_input.strip().lower()
    # loop over all oceans in hierarchy
    for ocean_name, data in hierarchy.items():
        # loop over all seas under this ocean
        for sea in data["seas"]:
            # if user input is part of sea name, return metadata
            if sea_input in sea["name"].strip().lower():
                return {
                    "name": sea["name"],
                    "ocean": ocean_name,
                    "alternate_names": sea.get("alternate_names", []),
                    "notes": sea.get("notes", "")
                }
    # if nothing matches, return none
    return None

# helper: find sea polygon from GeoJSON

def find_sea_polygon(sea_input):
    # normalize input
    sea_input = sea_input.strip().lower()
    # filter GeoDataFrame for any feature where names contains input
    matches = gdf[gdf["name"].str.lower().str.contains(sea_input)]
    return matches

# main lookup function

def lookup_sea():
    # ask user for sea name (partial also works)
    sea_input = input("Enter sea name (partial OK):").strip()
    if not sea_input:
        print(" No input given. Cancelled.")
        return
    
    # step 1: find metadata
    meta = find_sea_metadata(sea_input)
    if not meta:
        print("No metadata match found.")

    else:
        print("\n=== Sea Metadata ===")
        print(f"Name: {meta['name']}")
        print(f"Ocean: {meta['ocean']}")
        if meta['alternate_names']:
            print("Alternate names:", ", ".join(meta['alternate_names']))
        else:
            print("Alternate names: None")
        print(f"Notes: {meta['notes'] or 'None'}")
    
    # step 2: find polygons

    matches = find_sea_polygon(sea_input)
    if matches.empty:
        print("\n No polygon found for this sea.")
        return
    else:
        print("\n=== GeoJSON Match ===")
        print(matches[["name", "ocean"]])

        # step 3: plot matching polygons
        matches.plot(edgecolor="black", facecolor="lightblue")
        plt.title(", ".join(matches["name"].tolist()))
        plt.show()

# entry point

if __name__ == "__main__":
    lookup_sea()
    