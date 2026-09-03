"""Loads data/srd_spells.json into memory, keyed by lowercase spell name."""

from pathlib import Path
import json

DATA_PATH = Path(__file__).parent / "srd_spells.json"


def load_spells(path: Path = DATA_PATH) -> dict:
    with open(path, "r") as f:
        data = json.load(f)
        return {spell["name"].lower(): spell for spell in data}

def get_spell(spells: dict, name: str) -> dict | None:
    return spells.get(name.lower())

