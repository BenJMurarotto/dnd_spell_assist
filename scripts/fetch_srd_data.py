"""One-off: fetches SRD spell data (OGL/ORC-licensed, not full book text) to data/srd_spells.json so the app never hits the network at runtime."""
import json
from pathlib import Path

import requests

DATA_PATH = Path(__file__).parent.parent / "data" / "srd_spells.json"


def fetch_spells() -> list[dict]:
    session = requests.Session()
    response = session.get("https://www.dnd5eapi.co/api/spells", timeout=10)
    response.raise_for_status()
    data = response.json()

    full_spells = []
    for item in data["results"]:
        url = "https://www.dnd5eapi.co" + item["url"]
        spell_response = session.get(url, timeout=10)
        spell_response.raise_for_status()
        full_spells.append(spell_response.json())
    return full_spells



def write_cache(spells: list[dict], path: Path = DATA_PATH) -> None:
    with open(path, "w") as f:
        json.dump(spells, f, indent=2)


def main() -> None:
    data = fetch_spells()
    write_cache(spells=data, path=DATA_PATH)



if __name__ == "__main__":
    main()
