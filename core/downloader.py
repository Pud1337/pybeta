import yt_dlp
from pathlib import Path
from typing import Callable, Optional

def download(url: str, output_dir: str, audio_only: bool=False,
                progress_callback: Optional[Callable[[dict], None]] = None) -> str:
    output_template = str(Path(output_dir) / "%(title)s.%(ext)s")

    def hook(d):
        if progress_callback:
            progress_callback(d)

    ydl_opts = {
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": True,
        "progress_hooks": [hook],
    }

    if audio_only:
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        ydl_opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if audio_only:
            filename = str(Path(filename).with_suffix(".mp3"))
        return filename