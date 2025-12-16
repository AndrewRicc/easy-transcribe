import argparse
import os
import shutil
import sys
import traceback
import torch
import whisper
from dotenv     import load_dotenv
from pathlib    import Path

load_dotenv()

# ================= ARGUMENTS =================
parser = argparse.ArgumentParser(description="Transcribe audio to text using Whisper")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-b", "--bulk", action="store_true", help="Convert all videos in the video folder")
group.add_argument("video", nargs="?", type=Path, help="Path of the single video file")
args = parser.parse_args()

# === CONFIG ===
BASE_DIR = Path(__file__).parent
AUDIO_DIR = BASE_DIR / "audio"
TEXT_DIR = BASE_DIR / "text"
DONE_DIR = BASE_DIR / "audio_done"

MODEL = os.getenv("WHISPER_MODEL", "medium")   # tiny | base | small | medium | large
LANG = "it"

AUDIO_EXT = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}

# =================

TEXT_DIR.mkdir(exist_ok=True)
DONE_DIR.mkdir(exist_ok=True)

model = whisper.load_model(MODEL)
model = model.to("cuda") if torch.cuda.is_available() else model.to("cpu")

if args.bulk:
    audio_files = [
        f for f in AUDIO_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in AUDIO_EXT
    ]

    if not audio_files:
        print("No file audio found.")
        raise SystemExit(0)
else:
    audio_path = args.video.resolve()

    if not audio_path.exists():
        print(f"File not found: {audio_path}")
        sys.exit(1)

    if audio_path.suffix.lower() not in AUDIO_EXT:
        print("Format audio not supported.")
        sys.exit(1)

    audio_files = [audio_path]

for audio_path in audio_files:
    nome_base = audio_path.stem
    text_path = TEXT_DIR / f"{nome_base}.txt"
    done_path = DONE_DIR / audio_path.name

    print(f"Transcribing: {audio_path.name}")

    try:
        result = model.transcribe(str(audio_path), language=LANG)

        text_path.write_text(
            result["text"],
            encoding="utf-8"
        )

        if args.bulk or audio_path.parent == AUDIO_DIR:
            shutil.move(str(audio_path), str(done_path))
        print(f"✔ Saved: {text_path.name}")

    except Exception as e:
        print(f"❌ Error with {audio_path.name}: {e}")

print("All completed.")
