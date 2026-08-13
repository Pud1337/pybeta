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

def convert_media(input_path: str, outputh_path: str) -> str:
    out_ext = Path(outputh_path).suffix.lower().lstrip(".")
    cmd = [find_ffmpeg(), "-y", "-i", input_path]

    if out_ext == "mp3":
        cmd += ["-vn", "-acodec", "libmp3lame", "-q:a", "2"]
    elif out_ext == "mp4":
        cmd += ["-c:v", "libx264", "-c:a", "aac"]
    elif out_ext == "gif":
        cmd += ["-vf", "fps=15,scale=480:-1:flags=lanczos"]
    
    cmd.append(outputh_path)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{result.stderr}")
    return output_path

def convert(input_path: str, output_path: str) -> str:
    in_ext = Path(input_path).suffix.lower().lstrip(".")
    out_ext = Path(output_path).suffix.lower().lstrip(".")

    if in_ext in IMAGE_EXTS and out_ext in IMAGE_EXTS:
        return convert_image(input_path, output_path)
    elif in_ext in VIDEO_EXTS and out_ext in VIDEO_EXTS:
        return convert_media(input_path, output_path)
    else:
        raise ValueError(f"unsupported conversion: {in_ext} -> {out_ext}")