"""Pre-downloads the faster-whisper model for bundling into a packaged build. Run once before building: python scripts/download_model.py"""
from pathlib import Path

from faster_whisper import download_model

MODEL_SIZE = "tiny.en"
OUTPUT_DIR = Path(__file__).parent.parent / "models" / f"{MODEL_SIZE}_ct2"


def main() -> None:
    OUTPUT_DIR.parent.mkdir(exist_ok=True)
    path = download_model(MODEL_SIZE, output_dir=str(OUTPUT_DIR))
    print(f"Model downloaded to {path}")


if __name__ == "__main__":
    main()
