from __future__ import annotations

import itertools
from typing import List, Dict, Any, cast

from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from . import items
from . import locations
from . import creatures
from . import plants
from . import options
from .items import item_table, base_item_table, non_vehicle_depth_table, seamoth_table, prawn_table, cyclops_table, group_items, items_by_type, ItemType
from .rules import set_rules


class SubnauticaWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Subnautica randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Berserker"]
    )]


all_locations = {data["name"]: loc_id for loc_id, data in locations.location_table.items()}
all_locations.update(creatures.creature_locations)
all_locations.update(plants.plant_locations)


class SubnauticaWorld(World):
    """
    Subnautica is an undersea exploration game. Stranded on an alien world, you become infected by
    an unknown bacteria. The planet's automatic quarantine will shoot you down if you try to leave.
    You must find a cure for yourself, build an escape rocket, and leave the planet.
    """
    game = "Subnautica"
    web = SubnauticaWeb()

    item_name_to_id = {data.name: item_id for item_id, data in items.item_table.items()}
    location_name_to_id = all_locations
    options_dataclass = options.SubnauticaOptions
    options: options.SubnauticaOptions
    required_client_version = (0, 6, 2)
    origin_region_name = "Planet 4546B"
    creatures_to_scan: List[str]
    plants_to_scan: List[str]

    def generate_early(self) -> None:
        if not self.options.filler_items_distribution.weights_pair[1][-1]:
            raise Exception("Filler Items Distribution needs at least one positive weight.")
        if self.options.early_seaglide:
            self.multiworld.local_early_items[self.player]["Seaglide Fragment"] = 2

        scan_option: options.AggressiveScanLogic = self.options.creature_scan_logic
        creature_pool = scan_option.get_pool()
        plant_pool = self.options.plant_scans.get_pool()

        self.options.creature_scans.value = min(
            len(creature_pool),
            self.options.creature_scans.value
        )

        self.options.plant_scans.value = min(
            len(plants.all_flora),
            self.options.plant_scans.value
        )

        self.creatures_to_scan = self.random.sample(
            creature_pool, self.options.creature_scans.value)

        self.plants_to_scan = self.random.sample(
            plant_pool, self.options.plant_scans.value)

    def create_regions(self):
        # Create Region
        planet_region = Region("Planet 4546B", self.player, self.multiworld)

        # Create regular locations
        location_names = itertools.chain((location["name"] for location in locations.location_table.values()),
                                         (creature + creatures.suffix for creature in self.creatures_to_scan),
                                         (plant for plant in self.plants_to_scan))
        for location_name in location_names:
            loc_id = self.location_name_to_id[location_name]
            location = SubnauticaLocation(self.player, location_name, loc_id, planet_region)
            planet_region.locations.append(location)

        # Create events
        goal_event_name = self.options.goal.get_event_name()

        # only create one event (the victory)
        for event in locations.events:
            if event == goal_event_name:
                location = SubnauticaLocation(self.player, event, None, planet_region)
                location.place_locked_item(
                    SubnauticaItem(event, ItemClassification.progression, None, player=self.player))
                location.item.name = "Victory"
                planet_region.locations.append(location)

        # Register region to multiworld
        self.multiworld.regions.append(planet_region)

    # refer to rules.py
    set_rules = set_rules

    def get_theoretical_swim_depth(self):
        depth: int = 600
        consider_items: bool = False
        seaglide_depth: int = 200
        if self.options.swim_rule.value > 999:
            depth = int(self.options.swim_rule.value / 10)
            consider_items = self.options.swim_rule.value > 999
        else:
            depth = self.options.swim_rule.value
            consider_items = self.options.consider_items.value

        if self.options.classic.value:
            seaglide_depth: int = self.options.seaglide_depth.value

        if consider_items:
            return depth + seaglide_depth + 150
        return depth

    def create_items(self):
        # Generate item pool
        pool: List[SubnauticaItem] = []
        extras = self.options.creature_scans.value + self.options.plant_scans.value

        grouped = set(itertools.chain.from_iterable(group_items.values()))

        for item_id, item in base_item_table.items():
            if item_id in grouped:
                extras += item.count
            else:
                for _ in range(item.count):
                    subnautica_item = self.create_item(item.name)
                    if item.name == "Neptune Launch Platform":
                        if self.options.goal.get_event_name() == "Neptune Launch":
                            self.get_location("Aurora - Captain Data Terminal").place_locked_item(subnautica_item)
                        else:
                            pool.append(subnautica_item)
                    elif item.name == "Cyclops Shield Generator":
                        if self.options.include_cyclops.value == 2 and self.options.goal.get_event_name() != "Neptune Launch":
                            extras += 1
                        else:
                            pool.append(subnautica_item)
                    else:
                        pool.append(subnautica_item)

        for item_id, item in seamoth_table.items():
            if self.options.include_seamoth.value < 2:
                for _ in range(item.count):
                    pool.append(self.create_item(item.name))
            else:
                extras += item.count

        for item_id, item in prawn_table.items():
            if self.options.include_prawn.value < 2:
                for _ in range(item.count):
                    pool.append(self.create_item(item.name))
            else:
                extras += item.count

        for item_id, item in cyclops_table.items():
            if self.options.include_cyclops.value < 2:
                for _ in range(item.count):
                    pool.append(self.create_item(item.name))
            else:
                extras += item.count

        # If we can't make the necessary depth by traditional (vehicle) means, use the alternates
        # Shift the items to progression as part of that change
        seamoth_can_make_it: bool = False
        if self.options.include_seamoth.value == 0 and self.get_theoretical_swim_depth() + 900 > 1443:
            seamoth_can_make_it = True

        advanced_logic: bool = False
        if seamoth_can_make_it is False and self.options.include_prawn.value > 0 and \
                self.options.include_cyclops.value > 0:
            advanced_logic = True

        for item_id, item in non_vehicle_depth_table.items():
            for _ in range(item.count):
                if advanced_logic:
                    pool.append(self.create_shifted_item(item.name, ItemClassification.progression))
                else:
                    pool.append(self.create_item(item.name))

        group_amount: int = 2
        assert len(group_items) * group_amount <= extras
        for item_id in group_items:
            name = item_table[item_id].name
            for _ in range(group_amount):
                pool.append(self.create_item(name))
            extras -= group_amount

        # list of high-count important fragments as priority filler
        num = 2
        priority_filler: List[str] = [
            "Modification Station Fragment",
            "Laser Cutter Fragment",
        ]

        # There are edge cases where we don't need these; don't make extra priority filler if we don't need them
        # We're wasting a single item here with moonpool fragments for the Cyclops... meh
        if self.options.include_seamoth.value < 2 or \
                self.options.include_prawn.value < 2 or \
                self.options.include_cyclops.value < 2 or \
                self.options.goal.get_event_name() == "Neptune Launch":
            num += 2
            priority_filler.append("Mobile Vehicle Bay Fragment")
            priority_filler.append("Moonpool Fragment")

        # Vehicle priority filler
        if self.options.include_seamoth.value < 2:
            priority_filler.append("Seamoth Fragment")
            num += 1
        if self.options.include_prawn.value < 2:
            priority_filler.append("Prawn Suit Fragment")
            num += 1
        if self.options.include_cyclops.value < 2:
            priority_filler.append("Cyclops Engine Fragment")
            priority_filler.append("Cyclops Hull Fragment")
            priority_filler.append("Cyclops Bridge Fragment")
            num += 3
        if advanced_logic:
            # Thermal Plant has an unfair advantage; add some non-thermal-plant items
            # so that hopefully these are more common
            priority_filler.append("Multipurpose Room")
            priority_filler.append("Large Room")
            priority_filler.append("Nuclear Reactor Fragment")
            priority_filler.append("Bioreactor Fragment")
            num += 4

        for item_name in self.random.sample(priority_filler, k=min(extras, num)):
            item = self.create_item(item_name)

            # Make sure if we make any non-vehicle items here that show up do so as progression
            for alt_item in non_vehicle_depth_table.values():
                if item_name == alt_item.name and advanced_logic:
                    item = self.create_shifted_item(item_name, ItemClassification.progression)

            pool.append(item)
            extras -= 1

        # resource bundle filler
        for _ in range(extras):
            item = self.create_filler()
            item = cast(SubnauticaItem, item)
            pool.append(item)

        self.multiworld.itempool += pool

    def fill_slot_data(self) -> Dict[str, Any]:
        vanilla_tech: List[str] = []

        slot_data: Dict[str, Any] = {}
        if self.options.classic.value:
            # Classic Swim Rule is a string
            classic_swim_rule[str] = "easy"
            temp_swim_rule: int = self.options.swim_rule.value
            if temp_swim_rule > 999:
                temp_swim_rule = int(temp_swim_rule / 10)
            if temp_swim_rule > 200 and temp_swim_rule <= 400:
                classic_swim_rule = "normal"
            elif temp_swim_rule > 400:
                classic_swim_rule = "hard"

            if self.options.swim_rule.value > 999 or \
                    (self.options.classic.value and self.options.consider_items.value):
                classic_swim_rule += "_items"

            slot_data = {
                "goal": self.options.goal.current_key,
                "swim_rule": classic_swim_rule,
                "vanilla_tech": vanilla_tech,
                "creatures_to_scan": self.creatures_to_scan,
                "death_link": self.options.death_link.value,
                "free_samples": self.options.free_samples.value,
            }
        else:
            slot_data = {
                "goal": self.options.goal.current_key,
                "swim_rule": self.options.swim_rule.value,
                "consider_items": self.options.consider_items.value,
                "early_seaglide": self.options.early_seaglide.value,
                "seaglide_depth": self.options.seaglide_depth.value,
                "pre_seaglide_distance": self.options.pre_seaglide_distance.value,
                "include_seamoth": self.options.include_seamoth.value,
                "include_prawn": self.options.include_prawn.value,
                "include_cyclops": self.options.include_cyclops.value,
                "vanilla_tech": vanilla_tech,
                "creatures_to_scan": self.creatures_to_scan,
                "plants_to_scan": self.plants_to_scan,
                "death_link": self.options.death_link.value,
                "free_samples": self.options.free_samples.value,
                "reduce_resource_clutter": self.options.reduce_resource_clutter.value,
                "ignore_radiation": self.options.ignore_radiation.value,
                "can_slip_through": self.options.can_slip_through.value,
            }

        return slot_data

    def create_item(self, name: str) -> SubnauticaItem:
        item_id: int = self.item_name_to_id[name]

        return SubnauticaItem(name,
                              item_table[item_id].classification,
                              item_id, player=self.player)

    def create_shifted_item(self, name: str, cls) -> SubnauticaItem:
        item_id: int = self.item_name_to_id[name]
        return SubnauticaItem(name, cls, item_id, player=self.player)

    def get_filler_item_name(self) -> str:
        item_names, cum_item_weights = self.options.filler_items_distribution.weights_pair
        return self.random.choices(item_names, cum_weights=cum_item_weights, k=1)[0]


class SubnauticaLocation(Location):
    game: str = "Subnautica"


class SubnauticaItem(Item):
    game: str = "Subnautica"
