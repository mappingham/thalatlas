import json

with open ('data/sample_hierarchy.json', 'r') as f:
    data = json.load(f)

for ocean, info in data.items():
    print(f"Ocean: {ocean}")
    for sea in info["seas"]:
        alt_names = ", ".join(sea.get("alternate_names", [])) or "none"
        print (f" Sea: {sea['name']} (also called {alt_names})")
        # now print subseas if they exist
        for subsea in sea.get("subseas", []):
            sub_alt = ", ".join(subsea.get("alternate_names", [])) or "none"
            print(f"  Subsea: {subsea['name']} (also called {sub_alt})")