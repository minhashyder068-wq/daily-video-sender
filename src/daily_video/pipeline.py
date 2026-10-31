from pathlib import Path
import yaml

from .diary import load_diary, make_scenes
from .omni import generate_video
from .tts import synthesize
from .art_style import render_scene
from .render import render_video
from .hashtags import make_hashtags

def run():
    cfg = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))
    diary = load_diary()
    scenes = make_scenes(diary)
    work = Path("output/work")
    work.mkdir(parents=True, exist_ok=True)

    prompt = f"""Create a polished daily-diary video in vertical 9:16 format.
Diary events:
{chr(10).join("- " + s for s in scenes)}

Visual style: {cfg.get("style", "cinematic illustration")}.
Use coherent scenes, natural camera movement, and visual continuity.
Audio/voice: include natural spoken narration following the diary, clear human-like delivery,
and suitable ambient sound. Keep speech intelligible and synchronized with the story.
Make it suitable for short-form social media."""

    try:
        video = generate_video(prompt, work / "omni.mp4")
        mode = "gemini-omni"
    except Exception as exc:
        print(f"Omni unavailable; using local fallback: {exc}")
        scene_paths = [render_scene(s, i + 1, work / "scenes") for i, s in enumerate(scenes)]
        audio = synthesize(diary, work / "narration.mp3", cfg.get("tts", {}).get("voice", "en-US-GuyNeural"))
        video = render_video(scene_paths, audio, Path("output/daily-video.mp4"), cfg.get("duration_seconds", 45))
        mode = "local-fallback"

    tags = make_hashtags(diary)
    result = {
        "video": str(video),
        "mode": mode,
        "aspect_ratio": cfg.get("aspect_ratio", "9:16"),
        "title": "Daily Diary",
        "description": diary,
        "hashtags": tags,
        "youtube_upload_enabled": bool(cfg.get("youtube", {}).get("upload", False)),
    }
    Path("output/metadata.txt").write_text(
        result["title"] + "\n\n" + result["description"] + "\n\n" + " ".join(tags),
        encoding="utf-8"
    )
    return result
