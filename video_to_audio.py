import subprocess
import argparse
import shutil
import sys
from pathlib import Path

# ================= ARGUMENTS =================
parser = argparse.ArgumentParser(description="Convert video in audio mp3 with ffmpeg")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-b", "--bulk", action="store_true", help="Convert all videos in the video folder")
group.add_argument("video", nargs="?", type=Path, help="Path of the single video file")
parser.add_argument("prefix", type=str, help="Prefix for audio filenames")
parser.add_argument("index", type=int, help="Initial index")
args = parser.parse_args()

PREFIX = args.prefix
INDEX = args.index

# ================= PATH =================
BASE_DIR = Path(__file__).parent
VIDEO_DIR = BASE_DIR / "video"
VIDEO_DONE_DIR = BASE_DIR / "video_done"
AUDIO_DIR = BASE_DIR / "audio"

# Create folders if not exist
AUDIO_DIR.mkdir(exist_ok=True)
VIDEO_DONE_DIR.mkdir(exist_ok=True)

# Video extensions to consider
VIDEO_EXT = {".mp4", ".mkv", ".mov", ".avi"}

# ================= FIND VIDEO ORDED PER DATA =================
if args.bulk:
    video_files = sorted(
        [f for f in VIDEO_DIR.iterdir() if f.is_file() and f.suffix.lower() in VIDEO_EXT],
        key=lambda x: x.stat().st_birthtime
    )

    if not video_files:
        print("No video found in", VIDEO_DIR)
        raise SystemExit(0)
else:
    video_path = args.video.resolve()

    if not video_path.exists():
        print(f"File not found: {video_path}")
        sys.exit(1)

    if video_path.suffix.lower() not in VIDEO_EXT:
        print("Format video not supported.")
        sys.exit(1)

    video_files = [video_path]

# ================= LOOP CONVERSION =================
for video_path in video_files:
    output_name = f"{PREFIX}{INDEX}.mp3"
    output_path = AUDIO_DIR / output_name

    print(f"Converting: {video_path.name} → {output_name}")

    try:
        subprocess.run([
            "ffmpeg",
            "-y",  # override if exists
            "-i", str(video_path),
            "-vn",  # no video
            "-acodec", "libmp3lame",
            "-q:a", "2",
            str(output_path)
        ], check=True)

        # Move video file to done folder
        if args.bulk or video_path.parent == VIDEO_DIR:
            shutil.move(str(video_path), str(VIDEO_DONE_DIR / video_path.name))

        print(f"✔ Saved: {output_path.name}, video moved to video_done/")
        INDEX += 1

    except subprocess.CalledProcessError as e:
        print(f"❌ Error during conversion of {video_path.name}: {e}")

print("Conversion completed.")