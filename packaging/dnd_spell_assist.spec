# PyInstaller spec for a fully offline macOS .app bundle.
#
# Build (from repo root, after running scripts/download_model.py once):
#   pyinstaller packaging/dnd_spell_assist.spec --noconfirm
#
# Output: dist/D&D Spell Assist.app

import os

from PyInstaller.utils.hooks import collect_all

block_cipher = None

REPO_ROOT = os.path.abspath(os.path.join(SPECPATH, ".."))

datas = [
    (os.path.join(REPO_ROOT, "data", "srd_spells.json"), "data"),
    (os.path.join(REPO_ROOT, "models", "tiny.en_ct2"), "models/tiny.en_ct2"),
]
binaries = []
hiddenimports = []

for pkg in ("sounddevice", "ctranslate2", "faster_whisper", "webrtcvad"):
    pkg_datas, pkg_binaries, pkg_hiddenimports = collect_all(pkg)
    datas += pkg_datas
    binaries += pkg_binaries
    hiddenimports += pkg_hiddenimports

a = Analysis(
    [os.path.join(REPO_ROOT, "main.py")],
    pathex=[REPO_ROOT],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="D&D Spell Assist",
    debug=False,
    strip=False,
    upx=False,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="D&D Spell Assist",
)
app = BUNDLE(
    coll,
    name="D&D Spell Assist.app",
    icon=None,
    bundle_identifier="com.dndspellassist.app",
    info_plist={
        "NSMicrophoneUsageDescription": "D&D Spell Assist listens for spell "
        "names spoken during play to look up their rules text.",
    },
)
