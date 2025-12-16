# Easy-transcribe
Transcribe any audio to text and any video to audio

## venv setup
`python -m venv venv`

### Windows
`venv/Scripts/Activate.ps1`

### Bash
`source venv/bin/activate`

### for CUDA support (optional)
`python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130`

---

`python -m pip install openai-whisper`

Write your `.env` file

## Usage
This project is meant to work using `video_to_audio.py` -> `audio_to_text.py` in order to work properly, but you can the modules individually

### Video to Audio
This module uses FFMPEG to convert `{".mp4", ".mkv", ".mov", ".avi"}` these video extensions into `.mp3`.<br>
Using `-b` or `--bulk` argument it will convert all videos in the `video` directory.
---
If you don't use `-b` or `--bulk` argument you have to specify the video file path to convert.<br>
In all cases you have to specify also the name `prefix` and the initial `index`:
- prefix is the name prefix .mp3 files will have;
- index is the index suffix .mp3 files will have (default 1), assuming the script will convert all the videos in order of creation date and assuming you're allowed to convert video session by session.<br>
All video converted will be moved to `video_done` directory.

# Audio to Text
This module uses `openai-whisper` to transcribe audio to text.<br>
Using `-b` or `--bulk` argument it will convert all audios in the `audio` directory, `.txt` filename will be the same as the `.mp3` filename.
---
If you don't use `-b` or `--bulk` argument you have to specify the audio file path to transcribe.<br>
All audio transcribed will be moved to `audio_done` directory.<br>
This module supports cuda. Try the following snippet to see if cuda is available on your device.
```python
import torch
print(torch.cuda.is_available())
```
