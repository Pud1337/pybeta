import subprocess
import shutil
from pathlib import Path

from PIL import Image

IMAGE_EXTS = {"png", "jpg", "jpeg", "webp"}
VIDEO_EXTS = {"mp4", "mp3", "gif"}

def convert_image(input_path: str, output_path: str) -> str:
    img = Image.open(input_path)
    out_ext = Path(output_path).suffix.lower().lstrip(".")

    if out_ext in ("jpg", "jpeg") and img.mode in ("RGBA", "P"):
        img = img.convert("RGB") 

    img.save(output_path)
    return output_path 

def find_ffmpeg() -> str:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found, please install it before running.")
    return ffmpeg

def get_duration(input_path: str) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1", input_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def convert_media(input_path: str, output_path: str,
                   progress_callback: Optional[Callable[[str, float], None]] = None) -> str:
    duration = get_duration(input_path)
    out_ext = Path(output_path).suffix.lower().lstrip(".")
    cmd = [find_ffmpeg(), "-y", "-i", input_path]

    if out_ext == "mp3":
        cmd += ["-vn", "-acodec", "libmp3lame", "-q:a", "2"]
    elif out_ext == "mp4":
        cmd += ["-c:v", "libx264", "-c:a", "aac"]
    elif out_ext == "gif":
        cmd += ["-vf", "fps=15,scale=480:-1:flags=lanczos"]

    cmd += ["-progress", "pipe:1", "-nostats", output_path]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        line = line.strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        if key == "out_time_ms" and progress_callback:
            try:
                seconds = int(value) / 1_000_000
                percent = min(seconds / duration, 1.0) if duration else 0
                progress_callback("Converting...", percent)
            except ValueError:
                pass
            
    process.wait()
    if process.returncode != 0:
        raise RuntimeError(f"ffmpeg failed with code {process.returncode}")
    return output_path

def convert(input_path: str, output_path: str) -> str:
    in_ext = Path(input_path).suffix.lower().lstrip(".")
    out_ext = Path(output_path).suffix.lower().lstrip(".")

    if in_ext in IMAGE_EXTS and out_ext in IMAGE_EXTS:
        return convert_image(input_path, output_path)
    elif in_ext in VIDEO_EXTS or out_ext in VIDEO_EXTS:
        return convert_media(input_path, output_path)
    else:
        raise ValueError(f"unsupported conversion: {in_ext} -> {out_ext}")