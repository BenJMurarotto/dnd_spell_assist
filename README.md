# D&D Spell Assist

A listening companion for your D&D table. Say a spell name out loud during
a session, and its full rules text — level, school, casting time, range,
duration, description — pops up in the app!

## Using it

1. Download the app from the [Releases](../../releases) page and unzip it.
2. Double-click **D&D Spell Assist.app** to launch it. (First launch only:
   macOS will warn it's from an unidentified developer — right-click the
   app and choose **Open** instead of double-clicking to get past that.)
3. Grant microphone access when prompted.
4. Play as normal. Whenever anyone says a spell name, its details appear
   in the window.

No Python, no installation, no internet connection required — everything
runs locally on your machine.

Spell data is from the D&D 5e SRD (System Reference Document), the subset
of D&D rules released as open content under OGL 1.0a / ORC — not the full
copyrighted rulebooks.

## Building it yourself

If you'd rather run it from source or build your own copy:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/fetch_srd_data.py   # populate data/srd_spells.json
python main.py
```

### Pipeline

```
mic -> VAD (skip silence) -> STT (rolling buffer) -> fuzzy match against
spell names -> lookup in local dict -> display in GUI
```

### Packaging a standalone build

```
pip install -r requirements-build.txt
python scripts/download_model.py            # bundle the STT model offline
pyinstaller packaging/dnd_spell_assist.spec --noconfirm
```

Output: `dist/D&D Spell Assist.app`, fully self-contained (no Python or
internet needed to run it).
