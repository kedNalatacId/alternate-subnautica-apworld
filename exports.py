"""Runnable module that exports data needed by the mod/client."""

if __name__ == "__main__":
    import json
    import math
    import sys
    import os

    # makes this module runnable from its world folder.
    sys.path.remove(os.path.dirname(__file__))
    new_home = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    os.chdir(new_home)
    sys.path.append(new_home)

    from worlds.subnautica.locations import Vector, location_table
    from worlds.subnautica.items import item_table, group_items, items_by_type
    from NetUtils import encode

    export_folder = os.path.join(new_home, "Subnautica Export")
    os.makedirs(export_folder, exist_ok=True)

    def in_export_folder(path: str) -> str:
        return os.path.join(export_folder, path)

    payload = {location_id: location_data["position"] for location_id, location_data in location_table.items()}
    with open(in_export_folder("locations.json"), "w") as f:
        json.dump(payload, f)


    payload = {
        # "LaserCutter" in Subnautica ID
        "761": [location_id for location_id, location_data
                in location_table.items() if location_data["need_laser_cutter"] and location_data.get("can_slip_through", 'none') not in ['laser', 'both']],
        # PropulsionCannon in Subnautica ID
        "757": [location_id for location_id, location_data in location_table.items()
            if location_data.get("need_propulsion_cannon", False) and location_data.get("can_slip_through", 'none') not in ['propulsion', 'both']],
    }
    with open(in_export_folder("logic.json"), "w") as f:
        json.dump(payload, f)

    itemcount = sum(item_data.count for item_data in item_table.values())
    assert itemcount == len(location_table), f"{itemcount} != {len(location_table)}"
    payload = {item_id: item_data.tech_type for item_id, item_data in item_table.items()}
    import json

    with open(in_export_folder("items.json"), "w") as f:
        json.dump(payload, f)

    with open(in_export_folder("group_items.json"), "w") as f:
        # encode to convert set to list
        f.write(encode(group_items))

    with open(in_export_folder("item_types.json"), "w") as f:
        json.dump(items_by_type, f)

    print(f"Subnautica exports dumped to {in_export_folder('')}")
