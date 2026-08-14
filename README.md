# pybeta

A small desktop app to download YouTube videos/audio and convert media and
image files between formats. Built with `customtkinter`, `yt-dlp`, and
`ffmpeg`.

## Features

- Download YouTube videos (mp4) or extract audio only (mp3)
- Convert between:
  - `mp4` ↔ `mp3`
  - `mp4` ↔ `gif`
  - `png` / `jpg` ↔ `webp`

## Requirements

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/) (and `ffprobe`, included with it) on your PATH

Verify ffmpeg is installed:
```bash
ffmpeg -version
ffprobe -version
```

## Install

```bash
git clone https://github.com/Pud1337/pybeta.git
cd pybeta

python -m venv venv

# activate
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows

pip install -r requirements.txt
```

## Run

```bash
python main.py
```

### Download tab
Paste a YouTube URL, optionally check "Audio only (mp3)", click **Download**.

Files save to your OS's default Downloads folder
(`~/Downloads` on Linux/macOS, `C:\Users\<you>\Downloads` on Windows) —
this is hardcoded via `Path.home() / "Downloads"` in `gui/app.py`, not
currently configurable from the UI. ( i probably wont do this, but hey its easy enough, so if you want to fork it and ask to pull ill take a look )

### Convert tab
Browse to a file, pick a target format, click **Convert**. Output saves
next to the input file with the new extension.

## Images

![](https://raw.githubusercontent.com/Pud1337/pybeta/refs/heads/main/images/download.png "pybeta download tab")

![](https://raw.githubusercontent.com/Pud1337/pybeta/refs/heads/main/images/convert.png "pybeta convert tab")

## Known limitations / possible WIP

- Download location isn't user-configurable yet (always `~/Downloads`)
- No batch/queue support — one file or URL at a time
- GIF conversion uses a simple filter chain (no two-pass palette
  generation), so quality/size isn't optimized
- No playlist support (`noplaylist: True` is set intentionally)

## Troubleshooting

- **`ModuleNotFoundError`** — venv isn't activated, or
  `pip install -r requirements.txt` wasn't run inside it
- **`ffmpeg not found on PATH`** — install ffmpeg for your OS and restart
  your terminal
- **yt-dlp JS runtime warning** — safe to ignore; install
  [deno](https://deno.com/) if you want it gone
- Conversion errors print ffmpeg's raw stderr in the status label —
  copy the failing command from `convert_media()` in `core/converter.py`
  and run it manually in a terminal to debug further

## Packaging ( optional, but recommended so you don't have to activate venv every time you want to run it )

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name pybeta main.py
```
ffmpeg is **not** bundled by this — it must still be installed separately
on the machine running the packaged executable.
