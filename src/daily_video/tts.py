import asyncio
from pathlib import Path
import edge_tts

def synthesize(text,out_path,voice='en-US-GuyNeural'):
    out_path=Path(out_path); out_path.parent.mkdir(parents=True,exist_ok=True)
    async def go(): await edge_tts.Communicate(text,voice).save(str(out_path))
    asyncio.run(go()); return out_path
