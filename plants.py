import functools
from typing import Dict, TypedDict, List

class Vector(TypedDict):
    x: float
    y: float
    z: float

class FloraDict(TypedDict):
    name: str
    position: Vector

all_flora: Dict[int, FloraDict] = {
    34100: { 'name': 'Acid Mushroom', 'position': {'x': 0, 'y': 0, 'z': 0} },
    34101: { 'name': 'Anchor Pods', 'position': {'x': -250, 'y': -99, 'z': -690} },
    34102: { 'name': 'Bloodroot', 'position': {'x': -1068, 'y': -378, 'z': -605} },
    34103: { 'name': 'Bloodvine', 'position': {'x': -807, 'y': -219, 'z': 892} },
    34104: { 'name': 'Blue Palm', 'position': {'x': 0, 'y': 0, 'z': 0} },
    34105: { 'name': 'Brine Lily', 'position': {'x': -1264, 'y': -649, 'z': -215} },
    34106: { 'name': 'Bulb Bush', 'position': {'x': 690, 'y': -137, 'z': 835} },
    34107: { 'name': 'Bulbo Tree', 'position': {'x': -707, 'y': 1, 'z': -1097} },
    34108: { 'name': 'Cave Bush', 'position': {'x': 358, 'y': -28, 'z': 1067} },
    34109: { 'name': 'Chinese Potato Plant', 'position': {'x': -707, 'y': 1, 'z': -1097} },
    34110: { 'name': 'Crab Claw Kelp', 'position': {'x': -1081, 'y': -713, 'z': -588} },
    34111: { 'name': 'Creepvine', 'position': {'x': 0, 'y': 0, 'z': 0} },
    34112: { 'name': 'Creepvine Seeds', 'position': {'x': 0, 'y': 0, 'z': 0} },
    34113: { 'name': 'Deep Shroom', 'position': {'x': -807, 'y': -219, 'z': 892} },
    34114: { 'name': 'Drooping Stingers', 'position': {'x': -318, 'y': -79, 'z': 247} },
    34115: { 'name': 'Eye Stalk', 'position': {'x': -34, 'y': -22, 'z': 411} },
    34116: { 'name': 'Fern Palm', 'position': {'x': -707, 'y': 1, 'z': -1097} },
    34117: { 'name': 'Furled Papyrus', 'position': {'x': -496, 'y': -114, 'z': -11} },
    34118: { 'name': "Gabe's Feather", 'position': {'x': -795, 'y': -239, 'z': -360} },
    34119: { 'name': 'Gel Sack', 'position': {'x': 432, 'y': 3, 'z': 1193} },
    34120: { 'name': 'Ghost Weed', 'position': {'x': -780, 'y': -234, 'z': 950} },
    34121: { 'name': 'Giant Cove Tree', 'position': { 'x': -860, 'y': -920, 'z': 340} },
    34122: { 'name': 'Grub Basket' ,'position': {'x': -707, 'y': 1, 'z': -1097} },
    34123: { 'name': 'Jaffa Cup', 'position': {'x': -707, 'y': 1, 'z': -1097} },
    34124: { 'name': 'Jellyshroom', 'position': {'x': -350, 'y': -152, 'z': -208} },
    34125: { 'name': 'Lantern Tree', 'position': {'x': -707, 'y': 1, 'z': -1097} },
    34126: { 'name': 'Marblemelon Plant', 'position': {'x': -707, 'y': 1, 'z': -1097} },
    34127: { 'name': 'Membrain Tree', 'position': {'x': -382, 'y': -133, 'z': -669} },
    34128: { 'name': 'Ming Plant', 'position': {'x': -707, 'y': 1, 'z': -1097} },
    34129: { 'name': 'Pink Cap', 'position': {'x': -707, 'y': 1, 'z': -1097} },
    34130: { 'name': 'Pygmy Fan', 'position': {'x': -670, 'y': -190, 'z': 714} },
    34131: { 'name': 'Redwort', 'position': {'x': 384, 'y': -87, 'z': 1013} },
    34132: { 'name': 'Regress Shell', 'position': {'x': 384, 'y': -87, 'z': 1013} },
    34133: { 'name': 'Rouge Cradle', 'position': {'x': -496, 'y': 114, 'z': -11} },
    34134: { 'name': 'Sea Crown', 'position': {'x': -797, 'y': -143, 'z': -152} },
    34135: { 'name': 'Speckled Rattler', 'position': {'x': -707, 'y': 1, 'z': -1097} },
    34136: { 'name': 'Spiked Horn Grass', 'position': {'x': 334, 'y': -87, 'z': 1013} },
    34137: { 'name': 'Spotted Dockleaf', 'position': {'x': 334, 'y': -87, 'z': 1013} },
    34138: { 'name': 'Sulfer Plant', 'position': {'x': 0, 'y': 0, 'z': 0} },
    34139: { 'name': 'Tiger Plant', 'position': {'x': -100, 'y': -100, 'z': -100} },
    34140: { 'name': 'Tree Leech', 'position': {'x': 363, 'y': -17, 'z': 1050} },
    34141: { 'name': 'Veined Nettle', 'position': {'x': 0, 'y': 0, 'z': 0} },
    34142: { 'name': 'Violet Beau', 'position': {'x': -496, 'y': -114, 'z': -11} },
    34143: { 'name': 'Voxel Shrub', 'position': {'x': -707, 'y': 1, 'z': -1097} },
    34144: { 'name': 'Writhing Weed', 'position': {'x': 0, 'y': 0, 'z': 0} }
}

suffix: str = " Scan"

plant_locations: Dict[str, int] = {
    data["name"] + suffix: loc_id for loc_id, data in all_flora.items()
}

all_plants_presorted: List[str] = [
    name for loc_id, name in all_flora.items()
]
