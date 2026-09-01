from pipeline.listener import SpellListener

listener = SpellListener(on_spell_detected=lambda spell: print(f"DETECTED: {spell['name']}"))
listener.start()