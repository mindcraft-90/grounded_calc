import itertools
import streamlit as st
from collections import defaultdict

# ============================================================
# ENEMY DATA
# ============================================================

EXCLUDED_ENEMIES: list[str] = [
    "ARC.R", "Assistant Manager", "Bee", "Bombadier Beetle", "Director Schmector",
    "Diving Bell Spider", "Firefly", "Hedge Broodmother", "Infected Broodmother",
    "Infected Gnat", "Infected Mite", "Infected Weevil", "Ladybug", "Larva",
    "Lawn Mite", "Mant", "Mantis", "Mosquito", "Orb Weaver Jr", "Red Soldier Ant",
    "Red Worker Ant", "RUZ.T", "Scarab", "Sickly Roly Poly", "Spiderling",
    "Stinkbug", "TAYZ.T", "Water Flea", "Wasp Queen",
]

ENEMY_DATA: dict[str, dict[str, dict[str, float]]] = {
    "Antlion":            {"type": {"Generic": -0.25, "Slashing":  0.25, "Stabbing":  0.00, "Chopping": -0.25, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.50, "Spicy": -0.50, "Salty":  0.50, "Sour":  0.00}},
    "ARC.R":              {"type": {"Generic":  0.25, "Slashing": -0.25, "Stabbing": -0.50, "Chopping": -0.50, "Busting":  0.50}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy":  0.00, "Salty":  0.25, "Sour":  0.50}},
    "Assistant Manager":  {"type": {"Generic": -0.50, "Slashing": -0.25, "Stabbing": -0.50, "Chopping": -0.50, "Busting":  0.25}, "coating": {"Mighty":  0.00, "Fresh": -0.25, "Spicy":  0.00, "Salty":  0.50, "Sour":  0.50}},
    "Bee":                {"type": {"Generic": -0.25, "Slashing":  0.25, "Stabbing":  0.00, "Chopping":  0.25, "Busting": -0.25}, "coating": {"Mighty":  0.00, "Fresh":  0.25, "Spicy":  0.00, "Salty":  0.00, "Sour":  0.00}},
    "Black Ox Beetle":    {"type": {"Generic":  0.00, "Slashing": -0.25, "Stabbing": -0.25, "Chopping": -0.25, "Busting":  0.25}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy":  0.00, "Salty":  0.25, "Sour":  0.00}},
    "Black Soldier Ant":  {"type": {"Generic":  0.00, "Slashing": -0.50, "Stabbing":  0.25, "Chopping": -0.25, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.50, "Spicy":  0.50, "Salty":  0.00, "Sour":  0.00}},
    "Black Widow":        {"type": {"Generic":  0.00, "Slashing":  0.00, "Stabbing":  0.00, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.50, "Spicy": -0.50, "Salty": -0.50, "Sour":  0.25}},
    "Black Widowling":    {"type": {"Generic": -0.25, "Slashing":  0.00, "Stabbing": -0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.25, "Spicy":  0.50, "Salty":  0.00, "Sour":  0.00}},
    "Black Worker Ant":   {"type": {"Generic":  0.00, "Slashing":  0.00, "Stabbing":  0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.50, "Spicy":  0.50, "Salty":  0.00, "Sour":  0.00}},
    "Bombadier Beetle":   {"type": {"Generic": -0.25, "Slashing":  0.00, "Stabbing":  0.00, "Chopping":  0.50, "Busting": -0.25}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy":  0.00, "Salty":  0.00, "Sour":  0.00}},
    "Director Schmector": {"type": {"Generic": -0.50, "Slashing": -0.25, "Stabbing": -0.50, "Chopping": -0.50, "Busting":  0.25}, "coating": {"Mighty":  0.00, "Fresh": -0.25, "Spicy": -0.50, "Salty":  0.00, "Sour":  0.25}},
    "Diving Bell Spider": {"type": {"Generic":  0.00, "Slashing":  0.50, "Stabbing": -0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.25, "Spicy":  0.00, "Salty":  0.50, "Sour":  0.00}},
    "Dust Mite":          {"type": {"Generic": -0.25, "Slashing":  0.00, "Stabbing":  0.25, "Chopping":  0.00, "Busting": -0.25}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy": -0.25, "Salty": -0.25, "Sour":  0.00}},
    "Fire Soldier Ant":   {"type": {"Generic":  0.00, "Slashing": -0.50, "Stabbing":  0.00, "Chopping": -0.25, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy": -0.75, "Salty":  0.00, "Sour":  0.00}},
    "Fire Worker Ant":    {"type": {"Generic":  0.00, "Slashing":  0.00, "Stabbing":  0.00, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy": -0.75, "Salty":  0.00, "Sour":  0.00}},
    "Firefly":            {"type": {"Generic": -0.50, "Slashing":  0.00, "Stabbing":  0.50, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy": -0.50, "Salty":  0.00, "Sour":  0.00}},
    "Green Shield Bug":   {"type": {"Generic": -0.25, "Slashing":  0.00, "Stabbing":  0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy": -0.75, "Salty":  0.00, "Sour":  0.00}},
    "Hedge Broodmother":  {"type": {"Generic":  0.00, "Slashing":  0.25, "Stabbing": -0.50, "Chopping": -0.25, "Busting": -0.25}, "coating": {"Mighty":  0.00, "Fresh": -0.50, "Spicy":  0.25, "Salty": -0.50, "Sour":  0.00}},
    "Infected Broodmother": {"type": {"Generic": 0.00, "Slashing":  0.00, "Stabbing":  0.00, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.25, "Spicy": -0.75, "Salty": -0.50, "Sour":  0.00}},
    "Infected Wolf Spider": {"type": {"Generic": 0.00, "Slashing":  0.25, "Stabbing": -0.50, "Chopping":  0.00, "Busting":  0.25}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy":  0.25, "Salty": -0.50, "Sour":  0.00}},
    "Infected Gnat":      {"type": {"Generic":  0.00, "Slashing":  0.00, "Stabbing":  0.00, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy":  0.00, "Salty":  0.00, "Sour":  0.00}},
    "Infected Ladybug":   {"type": {"Generic":  0.25, "Slashing":  0.00, "Stabbing": -0.25, "Chopping":  0.00, "Busting":  0.50}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy": -0.25, "Salty": -0.25, "Sour":  0.00}},
    "Infected Larva":     {"type": {"Generic": -0.50, "Slashing":  0.50, "Stabbing": -0.25, "Chopping": -0.25, "Busting": -0.25}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy": -0.25, "Salty": -0.25, "Sour":  0.00}},
    "Infected Mite":      {"type": {"Generic": -0.50, "Slashing":  0.50, "Stabbing": -0.25, "Chopping":  0.50, "Busting": -0.25}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy":  0.00, "Salty":  0.00, "Sour":  0.00}},
    "Infected Weevil":    {"type": {"Generic": -0.50, "Slashing":  0.00, "Stabbing": -0.25, "Chopping": -0.25, "Busting": -0.25}, "coating": {"Mighty":  0.00, "Fresh":  0.25, "Spicy":  0.25, "Salty":  0.25, "Sour":  0.00}},
    "Ladybird":           {"type": {"Generic":  0.25, "Slashing":  0.00, "Stabbing": -0.50, "Chopping":  0.00, "Busting":  0.25}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy": -0.25, "Salty": -0.25, "Sour":  0.00}},
    "Ladybird Larva":     {"type": {"Generic": -0.50, "Slashing": -0.50, "Stabbing":  0.25, "Chopping": -0.50, "Busting": -0.50}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy": -0.85, "Salty":  0.00, "Sour":  0.00}},
    "Ladybug":            {"type": {"Generic":  0.25, "Slashing":  0.00, "Stabbing": -0.25, "Chopping":  0.00, "Busting":  0.50}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy": -0.25, "Salty": -0.25, "Sour":  0.00}},
    "Larva":              {"type": {"Generic":  0.00, "Slashing":  0.00, "Stabbing":  0.00, "Chopping": -0.25, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy":  0.25, "Salty":  0.00, "Sour":  0.00}},
    "Lawn Mite":          {"type": {"Generic":  0.00, "Slashing":  0.00, "Stabbing":  0.25, "Chopping":  0.25, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy":  0.00, "Salty":  0.00, "Sour":  0.00}},
    "Mant":               {"type": {"Generic": -0.25, "Slashing":  0.25, "Stabbing":  0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy": -0.25, "Salty": -0.25, "Sour":  0.00}},
    "Mantis":             {"type": {"Generic":  0.00, "Slashing": -0.50, "Stabbing": -0.50, "Chopping": -0.25, "Busting": -0.50}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy": -0.50, "Salty":  0.25, "Sour":  0.00}},
    "Mosquito":           {"type": {"Generic": -0.50, "Slashing":  0.25, "Stabbing":  0.00, "Chopping":  0.25, "Busting": -0.50}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy":  0.00, "Salty":  0.00, "Sour":  0.00}},
    "Moth":               {"type": {"Generic": -0.50, "Slashing": -0.50, "Stabbing":  0.00, "Chopping":  0.00, "Busting": -0.50}, "coating": {"Mighty":  0.00, "Fresh":  0.25, "Spicy":  0.25, "Salty": -0.50, "Sour":  0.25}},
    "Orb Weaver":         {"type": {"Generic": -0.25, "Slashing":  0.00, "Stabbing": -0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.25, "Spicy":  0.50, "Salty":  0.00, "Sour":  0.00}},
    "Orb Weaver Jr":      {"type": {"Generic": -0.25, "Slashing":  0.00, "Stabbing": -0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.25, "Spicy":  0.50, "Salty":  0.00, "Sour":  0.00}},
    "Red Soldier Ant":    {"type": {"Generic":  0.00, "Slashing": -0.50, "Stabbing":  0.25, "Chopping": -0.25, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy":  0.50, "Salty":  0.00, "Sour":  0.00}},
    "Red Worker Ant":     {"type": {"Generic":  0.00, "Slashing":  0.00, "Stabbing":  0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy":  0.50, "Salty":  0.00, "Sour":  0.00}},
    "Roly Poly":          {"type": {"Generic":  0.00, "Slashing": -0.25, "Stabbing": -0.50, "Chopping": -0.25, "Busting":  0.50}, "coating": {"Mighty":  0.00, "Fresh":  0.25, "Spicy":  0.25, "Salty":  0.25, "Sour":  0.00}},
    "RUZ.T":              {"type": {"Generic":  0.00, "Slashing":  0.00, "Stabbing":  0.00, "Chopping":  0.00, "Busting":  0.50}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy":  0.00, "Salty":  0.00, "Sour":  0.00}},
    "Scarab":             {"type": {"Generic":  0.00, "Slashing":  0.00, "Stabbing":  0.00, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy":  0.50, "Salty":  0.50, "Sour":  0.50}},
    "Sickly Roly Poly":   {"type": {"Generic":  0.25, "Slashing": -0.25, "Stabbing": -0.50, "Chopping": -0.25, "Busting":  0.50}, "coating": {"Mighty":  0.00, "Fresh": -0.25, "Spicy":  0.25, "Salty": -0.25, "Sour":  0.00}},
    "Spiderling":         {"type": {"Generic": -0.25, "Slashing":  0.00, "Stabbing": -0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.25, "Spicy":  0.50, "Salty":  0.00, "Sour":  0.00}},
    "Spiny Water Flea":   {"type": {"Generic":  0.00, "Slashing":  0.00, "Stabbing":  0.25, "Chopping": -0.50, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.25, "Spicy":  0.00, "Salty":  0.00, "Sour":  0.50}},
    "Stinkbug":           {"type": {"Generic": -0.25, "Slashing":  0.00, "Stabbing":  0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy":  0.00, "Salty":  0.00, "Sour":  0.00}},
    "TAYZ.T":             {"type": {"Generic":  0.25, "Slashing": -0.25, "Stabbing": -0.50, "Chopping": -0.50, "Busting":  0.50}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy":  0.00, "Salty":  0.25, "Sour":  0.50}},
    "Termite King":       {"type": {"Generic": -0.25, "Slashing": -0.50, "Stabbing":  0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.50, "Spicy":  0.00, "Salty":  0.25, "Sour":  0.00}},
    "Termite Worker":     {"type": {"Generic": -0.25, "Slashing": -0.50, "Stabbing":  0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy": -0.50, "Salty":  0.50, "Sour":  0.00}},
    "Termite Soldier":    {"type": {"Generic": -0.25, "Slashing": -0.50, "Stabbing":  0.25, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy": -0.50, "Salty":  0.50, "Sour":  0.00}},
    "Tick":               {"type": {"Generic": -0.25, "Slashing":  0.00, "Stabbing":  0.00, "Chopping":  0.00, "Busting": -0.50}, "coating": {"Mighty":  0.00, "Fresh": -0.50, "Spicy":  0.50, "Salty": -0.50, "Sour":  0.00}},
    "Tiger Mosquito":     {"type": {"Generic": -0.50, "Slashing":  0.25, "Stabbing":  0.00, "Chopping":  0.25, "Busting": -0.50}, "coating": {"Mighty":  0.00, "Fresh":  0.50, "Spicy":  0.00, "Salty":  0.00, "Sour":  0.00}},
    "Wasp":               {"type": {"Generic":  0.00, "Slashing":  0.00, "Stabbing": -0.50, "Chopping": -0.25, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy":  0.00, "Salty":  0.50, "Sour":  0.00}},
    "Wasp Drone":         {"type": {"Generic":  0.00, "Slashing":  0.00, "Stabbing": -0.50, "Chopping": -0.25, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy":  0.00, "Salty":  0.50, "Sour":  0.00}},
    "Wasp Queen":         {"type": {"Generic":  0.00, "Slashing": -0.25, "Stabbing": -0.50, "Chopping": -0.25, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh":  0.00, "Spicy": -0.25, "Salty":  0.25, "Sour":  0.00}},
    "Water Flea":         {"type": {"Generic":  0.00, "Slashing": -0.50, "Stabbing":  0.50, "Chopping":  0.00, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.25, "Spicy":  0.00, "Salty":  0.50, "Sour":  0.00}},
    "Wolf Spider":        {"type": {"Generic": -0.50, "Slashing":  0.25, "Stabbing": -0.50, "Chopping":  0.25, "Busting":  0.00}, "coating": {"Mighty":  0.00, "Fresh": -0.25, "Spicy":  0.50, "Salty":  0.00, "Sour":  0.00}},
}

DAMAGE_TYPES_ALL = ["Slashing", "Stabbing", "Chopping", "Busting"]
COATINGS_ALL     = ["Mighty", "Fresh", "Spicy", "Salty", "Sour"]
DAMAGE_TYPES_SET = set(DAMAGE_TYPES_ALL)
COATINGS_SET     = set(COATINGS_ALL)


# ============================================================
# CALCULATOR LOGIC
# ============================================================

def interpret_requirements(required_types):
    required_damage_types  = set()
    excluded_coatings      = set()
    owned_specific_combos  = set()
    for key, val in required_types:
        if key in DAMAGE_TYPES_SET:
            if val is None:
                required_damage_types.add(key)
            else:
                owned_specific_combos.add((key, val))
        elif key in COATINGS_SET:
            if val is None:
                excluded_coatings.add(key)
    return required_damage_types, excluded_coatings, owned_specific_combos


def build_preseed_coverage(excluded_coatings, owned_specific_combos, excluded_enemies, min_percent, type_modifiers):
    excluded_lower = [e.lower() for e in excluded_enemies]
    pre_covered    = set()
    preseed_reasons = defaultdict(list)
    for enemy, data in ENEMY_DATA.items():
        if enemy.lower() in excluded_lower:
            continue
        t = data["type"]
        c = data["coating"]
        for coating in excluded_coatings:
            pct = round(c.get(coating, 0.0) * 100)
            if pct >= min_percent:
                pre_covered.add(enemy)
                preseed_reasons[enemy].append((f"Pure {coating}", pct))
        for (dtype, coating) in owned_specific_combos:
            pct = round((t.get(dtype, 0.0) + c.get(coating, 0.0)) * 100) + type_modifiers.get(dtype, 0)
            if pct >= min_percent:
                pre_covered.add(enemy)
                preseed_reasons[enemy].append((f"{dtype}+{coating}", pct))
    return pre_covered, preseed_reasons


def build_weapon_data(excluded_coatings, owned_specific_combos, excluded_enemies, min_percent, type_modifiers):
    excluded_lower = [e.lower() for e in excluded_enemies]
    skip_combos    = set(owned_specific_combos)
    for coating in excluded_coatings:
        for dtype in DAMAGE_TYPES_SET:
            skip_combos.add((dtype, coating))
    weapons = {}
    for enemy, data in ENEMY_DATA.items():
        if enemy.lower() in excluded_lower:
            continue
        t = data["type"]
        c = data["coating"]
        for dtype in DAMAGE_TYPES_ALL:
            for coating in COATINGS_ALL:
                if (dtype, coating) in skip_combos:
                    continue
                val = round((t.get(dtype, 0.0) + c.get(coating, 0.0)) * 100) + type_modifiers.get(dtype, 0)
                if val < min_percent:
                    continue
                wname = f"{dtype} + {coating}"
                if wname not in weapons:
                    weapons[wname] = {"type": dtype, "augment": coating, "bugs": set(), "score": 0}
                weapons[wname]["bugs"].add(enemy)
                weapons[wname]["score"] += val
    return weapons


def remove_dominated_weapons(weapons, required_damage_types):
    names = list(weapons.keys())
    dominated = set()
    type_counts = defaultdict(int)
    for w in weapons.values():
        type_counts[w["type"]] += 1
    for a in names:
        for b in names:
            if a == b or b in dominated:
                continue
            if weapons[a]["type"] != weapons[b]["type"]:
                continue
            if weapons[b]["bugs"].issubset(weapons[a]["bugs"]) and weapons[a]["score"] >= weapons[b]["score"]:
                type_b = weapons[b]["type"]
                if type_b in required_damage_types and type_counts[type_b] <= 1:
                    continue
                dominated.add(b)
                type_counts[type_b] -= 1
    return {k: v for k, v in weapons.items() if k not in dominated}


def evaluate_loadout(combo, weapons, pre_covered, type_modifiers):
    already_covered = set(pre_covered)
    total_score = 0
    for weapon in sorted(combo, key=lambda w: weapons[w]["score"], reverse=True):
        new_bugs = weapons[weapon]["bugs"] - already_covered
        dtype, coating = weapons[weapon]["type"], weapons[weapon]["augment"]
        for enemy in new_bugs:
            data = ENEMY_DATA[enemy]
            val  = round((data["type"].get(dtype, 0.0) + data["coating"].get(coating, 0.0)) * 100) + type_modifiers.get(dtype, 0)
            total_score += val
        already_covered |= weapons[weapon]["bugs"]
    net_covered = already_covered - pre_covered
    return {"weapons": combo, "coverage": len(net_covered), "covered_bugs": net_covered, "score": total_score}


def valid_loadout(combo, weapons, required_damage_types):
    if not required_damage_types:
        return True
    return required_damage_types.issubset({weapons[w]["type"] for w in combo})


def find_best_loadout(weapons, pre_covered, required_damage_types, effective_size, type_modifiers):
    weapon_names = list(weapons.keys())
    best = None
    for size in range(1, effective_size + 1):
        for combo in itertools.combinations(weapon_names, size):
            if not valid_loadout(combo, weapons, required_damage_types):
                continue
            result = evaluate_loadout(combo, weapons, pre_covered, type_modifiers)
            if best is None:
                best = result
                continue
            if result["coverage"] > best["coverage"]:
                best = result
            elif result["coverage"] == best["coverage"]:
                if len(result["weapons"]) < len(best["weapons"]):
                    best = result
                elif len(result["weapons"]) == len(best["weapons"]) and result["score"] > best["score"]:
                    best = result
    return best


def trim_soft_covered(best, weapons, pre_covered, required_damage_types, soft_threshold, type_modifiers):
    loadout = list(best["weapons"])
    changed = True
    while changed:
        changed = False
        for weapon in loadout:
            dtype = weapons[weapon]["type"]
            if dtype in required_damage_types:
                if not [w for w in loadout if w != weapon and weapons[w]["type"] == dtype]:
                    continue
            others      = [w for w in loadout if w != weapon]
            new_bugs    = weapons[weapon]["bugs"] - pre_covered
            unique_bugs = new_bugs - set().union(*(weapons[w]["bugs"] for w in others))
            if not unique_bugs:
                loadout.remove(weapon)
                changed = True
                break
            all_soft_covered = all(
                any(
                    round((ENEMY_DATA[bug]["type"].get(weapons[w]["type"], 0.0)
                           + ENEMY_DATA[bug]["coating"].get(weapons[w]["augment"], 0.0)) * 100)
                    + type_modifiers.get(weapons[w]["type"], 0) >= soft_threshold
                    for w in others
                )
                for bug in unique_bugs
            )
            if all_soft_covered:
                loadout.remove(weapon)
                changed = True
                break
    return evaluate_loadout(tuple(loadout), weapons, pre_covered, type_modifiers)


def format_bug_entries(bugs, weapon_name, weapons, loadout_weapons, pre_covered, soft_threshold, type_modifiers, min_percent):
    dtype   = weapons[weapon_name]["type"]
    coating = weapons[weapon_name]["augment"]
    modifier = type_modifiers.get(dtype, 0)
    others  = [w for w in loadout_weapons if w != weapon_name]
    entries = {}
    for bug in bugs:
        raw = round((ENEMY_DATA[bug]["type"].get(dtype, 0.0) + ENEMY_DATA[bug]["coating"].get(coating, 0.0)) * 100)
        entries[bug] = ("normal", raw + modifier)
    other_full_bugs = set().union(*(weapons[w]["bugs"] for w in others)) | pre_covered if others else pre_covered
    excluded_lower  = [e.lower() for e in EXCLUDED_ENEMIES]
    for bug in ENEMY_DATA:
        if bug in entries or bug in pre_covered:
            continue
        if bug.lower() in excluded_lower:
            continue
        raw = round((ENEMY_DATA[bug]["type"].get(dtype, 0.0) + ENEMY_DATA[bug]["coating"].get(coating, 0.0)) * 100)
        eff = raw + modifier
        if soft_threshold <= eff < min_percent and bug not in other_full_bugs:
            entries[bug] = ("soft", eff)
    return dict(sorted(entries.items()))


def run_calculator(min_percent, max_loadout_size, soft_threshold, type_modifiers, required_types, excluded_enemies):
    required_damage_types, excluded_coatings, owned_specific_combos = interpret_requirements(required_types)
    owned_count    = len(owned_specific_combos) + len(excluded_coatings)
    effective_size = max_loadout_size - owned_count

    pre_covered, preseed_reasons = build_preseed_coverage(
        excluded_coatings, owned_specific_combos, excluded_enemies, min_percent, type_modifiers)
    weapons = build_weapon_data(
        excluded_coatings, owned_specific_combos, excluded_enemies, min_percent, type_modifiers)

    excluded_lower = [e.lower() for e in excluded_enemies]
    all_reachable  = set(pre_covered) | set().union(*(w["bugs"] for w in weapons.values()))
    truly_uncoverable = sorted(
        e for e in ENEMY_DATA
        if not e.lower() in excluded_lower and e not in all_reachable
    )

    weapons = remove_dominated_weapons(weapons, required_damage_types)
    best    = find_best_loadout(weapons, pre_covered, required_damage_types, effective_size, type_modifiers)

    if not best:
        return None, pre_covered, preseed_reasons, truly_uncoverable, required_damage_types, excluded_coatings, owned_specific_combos, owned_count, effective_size, max_loadout_size, weapons

    best = trim_soft_covered(best, weapons, pre_covered, required_damage_types, soft_threshold, type_modifiers)

    return best, pre_covered, preseed_reasons, truly_uncoverable, required_damage_types, excluded_coatings, owned_specific_combos, owned_count, effective_size, max_loadout_size, weapons


# ============================================================
# STREAMLIT UI
# ============================================================

st.set_page_config(page_title="Grounded Loadout Calculator", layout="wide")

st.title("⚔️ Grounded Loadout Calculator")

# ── Sidebar: numeric settings only ───────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    min_percent = st.slider("Min Coverage %", min_value=25, max_value=100, value=50, step=25,
                             help="Minimum effective % for a weapon to count as covering an enemy.")
    max_loadout_size = st.slider("Max Loadout Size", min_value=1, max_value=10, value=6, step=1,
                                  help="Total weapon slots available.")
    soft_threshold = st.slider("Soft Cover Threshold %", min_value=0, max_value=50, value=25, step=25,
                                help="A weapon can be dropped if all its unique enemies are soft-covered at this % by another weapon.")

    st.divider()
    st.subheader("🔧 Type Modifiers")
    st.caption("Positive = bonus, Negative = penalty.")

    modifier_rows = {}
    for dtype in DAMAGE_TYPES_ALL:
        default = {"Busting": -25}.get(dtype, 0)
        modifier_rows[dtype] = st.number_input(dtype, min_value=-100, max_value=100, value=default, step=25, key=f"mod_{dtype}")

    type_modifiers = {k: v for k, v in modifier_rows.items() if v != 0}

# ── Main page: owned weapons ──────────────────────────────────
st.subheader("🎒 Owned Weapons & Requirements")
st.caption(
    "**Type + Coating** → you own this exact weapon (pre-seeds coverage).  \n"
    "**Type only** → loadout must include this damage type (any coating).  \n"
    "**Coating only** → you own a pure coating weapon (e.g. Mint Mace); pre-seeds coverage and removes that coating from the search."
)

if "required_rows" not in st.session_state:
    st.session_state.required_rows = [
        {"type": "Chopping", "coating": "Sour"},
        {"type": "Chopping", "coating": "— (type requirement only)"},
        {"type": "— (coating weapon)", "coating": "Fresh"},
    ]

TYPE_OPTIONS    = ["— (coating weapon)"] + DAMAGE_TYPES_ALL
COATING_OPTIONS = ["— (type requirement only)"] + COATINGS_ALL

rows_to_delete = []
for i, row in enumerate(st.session_state.required_rows):
    cols = st.columns([3, 3, 1])
    with cols[0]:
        t_val = st.selectbox("Type", TYPE_OPTIONS,
                             index=TYPE_OPTIONS.index(row["type"]) if row["type"] in TYPE_OPTIONS else 0,
                             key=f"rtype_{i}", label_visibility="collapsed")
    with cols[1]:
        c_val = st.selectbox("Coating", COATING_OPTIONS,
                             index=COATING_OPTIONS.index(row["coating"]) if row["coating"] in COATING_OPTIONS else 0,
                             key=f"rcoat_{i}", label_visibility="collapsed")
    with cols[2]:
        if st.button("✕", key=f"del_{i}"):
            rows_to_delete.append(i)
    st.session_state.required_rows[i] = {"type": t_val, "coating": c_val}

for i in sorted(rows_to_delete, reverse=True):
    st.session_state.required_rows.pop(i)

if st.button("＋ Add weapon"):
    st.session_state.required_rows.append({"type": DAMAGE_TYPES_ALL[0], "coating": "— (type requirement only)"})

# Parse rows into required_types tuples
required_types = []
for row in st.session_state.required_rows:
    t = row["type"]
    c = row["coating"]
    if t == "— (coating weapon)" and c != "— (type requirement only)":
        required_types.append((c, None))
    elif t != "— (coating weapon)":
        coating_val = None if c == "— (type requirement only)" else c
        required_types.append((t, coating_val))

# ── Main page: enemy exclusions ───────────────────────────────
st.divider()

all_enemy_names = sorted(ENEMY_DATA.keys())

if "excluded_enemies" not in st.session_state:
    st.session_state.excluded_enemies = sorted(EXCLUDED_ENEMIES)

with st.expander(f"🐛 Enemy Exclusions ({len(st.session_state.excluded_enemies)} excluded)", expanded=False):
    st.caption("Unchecked enemies are excluded from coverage calculations.")

    col_count = 4
    cols = st.columns(col_count)
    for idx, enemy in enumerate(all_enemy_names):
        currently_included = enemy not in st.session_state.excluded_enemies
        checked = cols[idx % col_count].checkbox(enemy, value=currently_included, key=f"enemy_{enemy}")
        if checked and enemy in st.session_state.excluded_enemies:
            st.session_state.excluded_enemies.remove(enemy)
        elif not checked and enemy not in st.session_state.excluded_enemies:
            st.session_state.excluded_enemies.append(enemy)

    ex_col1, ex_col2 = st.columns(2)
    with ex_col1:
        if st.button("✅ Include all"):
            st.session_state.excluded_enemies = []
            st.rerun()
    with ex_col2:
        if st.button("🔄 Reset to defaults"):
            st.session_state.excluded_enemies = sorted(EXCLUDED_ENEMIES)
            st.rerun()

active_excluded = st.session_state.excluded_enemies

st.divider()
run_btn = st.button("▶ Calculate", type="primary", use_container_width=True)

# ── Main panel ───────────────────────────────────────────────
if run_btn or "last_result" in st.session_state:
    if run_btn:
        with st.spinner("Searching loadouts…"):
            result = run_calculator(min_percent, max_loadout_size, soft_threshold, type_modifiers, required_types, active_excluded)
        st.session_state.last_result = result
        st.session_state.last_params = {
            "min_percent": min_percent, "max_loadout_size": max_loadout_size,
            "soft_threshold": soft_threshold, "type_modifiers": type_modifiers,
            "required_types": required_types,
        }

    (best, pre_covered, preseed_reasons, truly_uncoverable,
     required_damage_types, excluded_coatings, owned_specific_combos,
     owned_count, effective_size, max_ls, weapons) = st.session_state.last_result
    params = st.session_state.last_params

    excluded_lower = [e.lower() for e in active_excluded]
    total_bugs     = sum(1 for e in ENEMY_DATA if not e.lower() in excluded_lower)

    # ── Header summary ──
    col1, col2, col3 = st.columns(3)
    with col1:
        owned_labels = []
        if excluded_coatings:
            owned_labels.append("**Coating weapons:** " + ", ".join(sorted(excluded_coatings)))
        if owned_specific_combos:
            owned_labels.append("**Specific weapons:** " + ", ".join(f"{d}+{c}" for d, c in sorted(owned_specific_combos)))
        if required_damage_types:
            owned_labels.append("**Must include:** " + ", ".join(sorted(required_damage_types)))
        st.markdown("\n\n".join(owned_labels) if owned_labels else "*No owned weapons configured.*")
    with col2:
        st.metric("Slots searching", f"{effective_size} / {max_ls}")
        st.metric("Pre-covered", len(pre_covered))
    with col3:
        if best:
            total_covered = len(best["covered_bugs"]) + len(pre_covered)
            st.metric("Total coverage", f"{total_covered} / {total_bugs}")
            st.metric("Weapons used", len(best["weapons"]))

    st.divider()

    # ── Pre-covered ──
    if pre_covered:
        with st.expander(f"✅ Pre-covered ({len(pre_covered)} bugs)", expanded=False):
            rows = []
            for b in sorted(pre_covered):
                reasons = ", ".join(f"{label} ({pct:+d}%)" for label, pct in preseed_reasons[b])
                rows.append({"Enemy": b, "Covered by": reasons})
            st.table(rows)

    if not best:
        st.error("No valid loadout found.")
        st.stop()

    # ── Best loadout ──
    st.subheader("🏆 Best Loadout")

    coating_groups = defaultdict(list)
    for weapon in best["weapons"]:
        coating_groups[weapons[weapon]["augment"]].append(weapon)

    for weapon in best["weapons"]:
        data     = weapons[weapon]
        new_bugs = data["bugs"] - pre_covered
        shared   = data["bugs"] & pre_covered
        coating  = data["augment"]
        siblings = [w for w in coating_groups[coating] if w != weapon]

        entries = format_bug_entries(
            new_bugs, weapon, weapons, best["weapons"],
            pre_covered, params["soft_threshold"], params["type_modifiers"], params["min_percent"]
        )

        # Heading row
        badge = f"**{weapon}** &nbsp; `{len(new_bugs)} new` &nbsp; `{len(shared)} owned`"
        with st.expander(badge, expanded=True):
            # Sibling comparison
            for sibling in siblings:
                unique_to_this = new_bugs - weapons[sibling]["bugs"]
                unique_to_sib  = (weapons[sibling]["bugs"] - pre_covered) - data["bugs"]
                if unique_to_this or unique_to_sib:
                    st.caption(f"vs **{sibling}**")
                    if unique_to_this:
                        st.caption(f"&nbsp;&nbsp;Unique over {sibling}: {', '.join(sorted(unique_to_this))}")
                    if unique_to_sib:
                        st.caption(f"&nbsp;&nbsp;{sibling} uniquely covers: {', '.join(sorted(unique_to_sib))}")

            if entries:
                cols = st.columns(4)
                for idx, (bug, (kind, pct)) in enumerate(sorted(entries.items())):
                    label = f"{'🔶 soft ' if kind == 'soft' else ''}{pct:+d}%"
                    cols[idx % 4].markdown(f"**{bug}** {label}")
            else:
                st.caption("No new bugs covered.")

    # ── Summary ──
    st.divider()
    total_covered = len(best["covered_bugs"]) + len(pre_covered)
    not_covered   = sorted(
        e for e in ENEMY_DATA
        if not e.lower() in excluded_lower
        and e not in best["covered_bugs"] and e not in pre_covered
    )
    not_picked_up = [e for e in not_covered if e not in truly_uncoverable]

    st.markdown(f"**{len(best['weapons'])} weapons** &nbsp;|&nbsp; **{len(best['covered_bugs'])} new** + **{len(pre_covered)} owned** = **{total_covered}/{total_bugs}** bugs covered")

    c1, c2 = st.columns(2)
    with c1:
        if truly_uncoverable:
            st.warning(f"No weapon reaches {params['min_percent']}% ({len(truly_uncoverable)})")
            for b in truly_uncoverable:
                st.markdown(f"- {b}")
    with c2:
        if not_picked_up:
            st.info(f"Not worth a slot ({len(not_picked_up)})")
            for b in not_picked_up:
                st.markdown(f"- {b}")

else:
    st.info("Configure your settings in the sidebar and click **▶ Calculate**.")
