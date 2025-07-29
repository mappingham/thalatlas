# Add GEOJSON script:
    # Partial matching for ocean and seas (like in Add Entry)
    # Interactive prompt for coordinates
    # Automatically appends to sample_seas.geojson
    # Works if GeoJSON doesn't exist yet
    # Saves cleanly, ready for plotting

import json
from pathlib import Path

# paths
DATA_JSON = Path("data/sample_hierarchy.json")
GEOJSON_FILE = Path("data/sample_seas.geojson")

# load hierarchy JSON

if DATA_JSON.exists():
    with open(DATA_JSON, "r") as f:
        hierarchy = json.load(f)
else:
    print(" sample_hierarchy.json not found.")
    hierarchy = {}

# helper: load existing GeoJSON or create new

def load_geojson():
    if GEOJSON_FILE.exists():
        with open(GEOJSON_FILE, "r") as f:
            return json.load(f)
    else:
        return {"type": "FeatureCollection", "features": []}

def save_geojson(data):
    with open(GEOJSON_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f" Saved to {GEOJSON_FILE}")

# partial match helper for oceans
def match_ocean_name(user_input):
    user_input = user_input.strip().lower()
    matches = [o for o in hierarchy.keys() if user_input in o.lower()]
    if len(matches) == 1:
        print(f"Matched ocean: {matches[0]}")
        return matches[0]
    elif len(matches) > 1:
        print(" Multiple ocean matches:", ",".join(matches))
        return None
    else:
        print(" No ocean match found.")
        return None
# partial match helper for seas

def match_sea_name(ocean_name, user_input):
    seas = hierarchy[ocean_name]["seas"]
    user_input = user_input.strip().lower()
    matches = [s for s in seas if user_input in s["name"].strip().lower()]
    if len(matches) == 1:
        print(f"Matched sea: {matches[0]['name']}")
        return matches[0]["name"]
    elif len(matches) > 1:
        print(" Multiple sea matches:", ", ".join(s["name"] for s in matches))
        return None
    else:
        print(" No sea match found.")
        return None

# prompt for coordinates

def prompt_coordinates():
    print("Enter coordinates in 'lon,lat' format separated by semicolon.")
    print("Example: -80,15; -75,15; -75,20; -80,20; -80,15")
    coord_input = input("Coordinates: ".strip())
    if not coord_input:
        print(" No coordinates entered. Cancelled.")
        return None
    
    try:
        coords = []
        for pair in coord_input.split(";"):
            lon, lat = pair.strip().split(",")
            coords.append([float(lon), float(lat)])
        return coords
    except Exception as e:
        print(" Invalid coordinate format:", e)
        return None
    
def add_geojson_entry():
    # Step 1: pick ocean
    ocean_input = input("Which ocean? ").strip()
    ocean_name = match_ocean_name(ocean_input)
    if not ocean_name:
        return False

    # Step 2: pick sea
    seas = hierarchy[ocean_name]["seas"]
    if not seas:
        print(" No seas under this ocean. Add one first.")
        return False
        
    print ("Available seas:", ", ".join(s["name"] for s in seas))
    sea_input = input("Which sea? ").strip()
    sea_name = match_sea_name(ocean_name, sea_input)
    if not sea_name:
        return False
        
    # Step 3: get coordinates

    coords = prompt_coordinates()
    if not coords:
        return False
        
    # Step 4: build new GeoJSON feature
    feature = {
        "type": "Feature",
        "properties": {
            "name": sea_name,
            "ocean": ocean_name
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [coords]
        }
    }

    # Step 5: load existing GeoJSON & append

    geojson_data = load_geojson()
    geojson_data["features"].append(feature)

    # Step 6: save
    save_geojson(geojson_data)
    return True
    
def main_loop():
    while True:
        print("\n=== Thalatlas GeoJSON Add Entry ===")
        print("1. Add Sea Polygon")
        print("2. Quit")
        choice = input("Choose (1/2): ".strip())

        if choice == "1":
            result = add_geojson_entry()
            if result:
                print(" Polygon added.")
        elif choice == "2":
            print(" Exiting GeoJSON helper.")
            break
        else:
            print(" Invalid choice, try again.")

        again = input("Add another polygon? (y/n): ").strip().lower()
        if again != "y":
            print(" Done adding polygons.")
            break

if __name__ == "__main__":
    main_loop()