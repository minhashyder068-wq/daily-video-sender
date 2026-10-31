import base64
import os
from pathlib import Path
from google import genai

MODEL = "gemini-omni-1.1-flash"

def generate_video(prompt, out_path):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    client = genai.Client(api_key=api_key)
    interaction = client.interactions.create(model=MODEL, input=prompt)
    video = getattr(interaction, "output_video", None)
    data = getattr(video, "data", None) if video else None
    if not data:
        raise RuntimeError("Gemini Omni did not return output_video.data.")
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(data))
    return out
