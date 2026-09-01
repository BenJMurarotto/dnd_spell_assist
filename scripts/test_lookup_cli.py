"""Stage-1 sanity check: type a spell name, print its cached data.

Validates data/srd_spells.json and data/loader.py before any audio/STT
code exists.
"""
from data.loader import get_spell, load_spells



def main() -> None:
    data = load_spells()
    spell_name = input("Spell name: ")
    spell = get_spell(data, spell_name)

    if spell is None:
        print(f"No spell found for '{spell_name}'")
    else:
        print(spell)

if __name__ == "__main__": 
    main()