"""Loads the cached SRD spell dataset into memory for fast lookup.

Data source: data/srd_spells.json, populated by scripts/fetch_srd_data.py.
Kept in memory as a dict keyed by lowercase spell name — no DB round trip
at lookup time.
"""

from pathlib import Path
import json

DATA_PATH = Path(__file__).parent / "srd_spells.json"


def load_spells(path: Path = DATA_PATH) -> dict:
    with open(path, "r") as f:
        data = json.load(f)
        return {spell["name"].lower(): spell for spell in data}

def get_spell(spells: dict, name: str) -> dict | None:
    return spells.get(name.lower())

