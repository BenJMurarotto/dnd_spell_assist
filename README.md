# D&D Spell Assist

Listens via microphone during a D&D session; when a spell name is spoken,
looks it up from a locally cached SRD dataset and displays its details
(description, level, casting time, etc.) for the DM.

## Data

Spell data comes from the D&D 5e SRD (System Reference Document), which is
open content under OGL 1.0a / ORC — not the full copyrighted rulebooks.
Run `scripts/fetch_srd_data.py` once to populate `data/srd_spells.json`;
the app reads that local file at runtime, no network calls during use.

## Pipeline

```
mic -> VAD (skip silence) -> STT (rolling buffer) -> fuzzy match against
spell names -> lookup in local dict -> display in GUI
```

## Build order

1. `scripts/fetch_srd_data.py` + `data/loader.py` — validate the data cache
   via `scripts/test_lookup_cli.py` before any audio code exists.
2. `stt/transcriber.py` against a pre-recorded `.wav` — no mic yet.
3. `matching/spell_matcher.py` against that transcript.
4. `audio/capture.py` + `audio/vad.py` — swap in live mic, still
   console-only via `pipeline/listener.py`.
5. `ui/` — PySide6 window wired up last.

## Setup

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
