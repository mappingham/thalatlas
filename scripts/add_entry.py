import json
from pathlib import Path

DATA_FILE = Path("data/sample_hierarchy.json")

# Load existing JSON

if DATA_FILE.exists():
    with open(DATA_FILE, "r") as f:
        hierarchy = json.load(f)
else:
    hierarchy = {}

def save_json():
    with open(DATA_FILE, "w") as f:
        json.dump(hierarchy, f, indent=2)
    print("\n Changes saved to", DATA_FILE)

def match_ocean_name(user_input):
    """Try to match a partial input to an existing ocean name."""
    user_input = user_input.strip().lower()
    matches = [o for o in hierarchy.keys() if user_input in o.lower()]
    if len(matches) == 1:
        print(f"Matched: {matches[0]}")
        return matches[0]
    elif len(matches) > 1:
        print("Multiple matches:", ", ".join(matches))
        return None
    else:
        print(" No ocean match found.")
        return None

def match_sea_name(seas, user_input):
    """Try to match a partial sea name"""
    user_input = user_input.strip().lower()
    matches = [s for s in seas if user_input in s["name"].lower()]
    if len(matches) == 1:
        print(f"Matched: {matches[0]['name']}")
        return matches[0]
    elif len(matches) > 1:
        print(" Multiple sea matches:", ", ".join(s["name"] for s in matches))
        return None
    else:
        print(" No sea match found.")
        return None

def add_ocean():
    ocean_name = input("New ocean name (leave blank to cancel):").strip()
    if not ocean_name:
        print("  No ocean name entered. Cancelled.")
        return False
    if ocean_name in hierarchy:
        print(" Ocean already exists.")
        return
    hierarchy[ocean_name] = {"seas": []}
    print(f" Added ocean: {ocean_name}")
    return True

def add_sea():
    ocean_input = input("Which ocean does this sea belong to? ").strip()
    ocean_name = match_ocean_name(ocean_input)

    if not ocean_name:
        return False # stop if no match

  
    
    sea_name = input("Sea name (leave blank to cancel): ").strip()
    if not sea_name:
        print(" No sea name entered. Cancelled.")
        return False
    
    alt_names = input("Alternate names (comma separated, or leave blank): ").strip()
    notes = input("Notes: ").strip()

    sea_entry = {
        "name": sea_name,
        "alternate_names": [n.strip() for n in alt_names.split(",")] if alt_names else [],
        "notes": notes,
        "subseas": []
    }

    hierarchy[ocean_name]["seas"].append(sea_entry)
    print(f" Added sea '{sea_name}' under {ocean_name}")
    return True

def add_subsea():
    ocean_input = input("Which ocean does this sea belong to? ").strip()
    ocean_name = match_ocean_name(ocean_input)
    if not ocean_name:
        return False  # stop if no match
    
    seas = hierarchy[ocean_name]["seas"]

    if not seas:
        print(" No seas found under this ocean yet; add sea first.")
        return False
    
    # Show available seas
    sea_names = [s["name"] for s in seas]
    print("Available seas:", ", ".join(sea_names))
    sea_input = input("Which sea does this subsea belong to? ").strip().lower()

    print("DEBUG: sea_input=", sea_input)
    print("DEBUG: testing each sea...")

    for s in seas:
        sea_clean = s["name"].strip().lower()
        print(f" checking: {sea_clean} contains {sea_input}? ->", sea_input in sea_clean)
    
    # robust matching (strip + lowercase)

    matches = [s for s in seas if sea_input in s["name"].strip().lower()]
    print("DEBUG: matches found=", [s["name"] for s in matches])

    if len(matches) == 1:
        sea = matches[0]
        print(f"Matched: {sea['name']}")
    elif len(matches) > 1:
        print(" Multiple sea matches:", ", ".join(s["name"] for s in matches))
        return False
    else:
        print(" No sea match found.")
        return False

    # Find matching sea (partial match allowed)
    #sea = match_sea_name(seas, sea_input)
    #if not sea:
        #return False
    
    # Proceed only if a single sea was matched
    subsea_name = input("Subsea name: (leave blank to cancel): ").strip()
    if not subsea_name:
        print(" No subsea name entered. Cancelled.")
        return False
    
    alt_names = input("Alternate names (comma separated or leave blank): ").strip()
    notes = input("Notes: ").strip()

    subsea_entry = {
        "name": subsea_name,
        "alternate_names": [n.strip() for n in alt_names.split(",")] if alt_names else [],
        "notes": notes
    }
    sea["subseas"].append(subsea_entry)
    print(f" Added subsea '{subsea_name}' under {sea['name']}")
    return True


def main_loop():
    while True:
        print("\n=== Thalatlas Add Entry ===")
        print("1. Add Ocean")
        print("2. Add Sea")
        print("3. Add Subsea")
        print("4. Quit")
        choice = input("Choose (1/2/3/4): ").strip()

        result = False # track if we added something

        if choice == "1":
            add_ocean()
        elif choice == "2":
            add_sea()
        elif choice == "3":
            add_subsea()
        elif choice == "4":
            print(" Exiting.")
            break
        else:
            print(" Invalid choice, try again.")
            continue
    
        # Save after making a change
        if result:
            save_json() # only save if something was added

        again = input("Add another? (y/n): ").strip().lower()
        if again != "y":
            print(" Done adding entries.")
            break

if __name__ == "__main__":
    main_loop()