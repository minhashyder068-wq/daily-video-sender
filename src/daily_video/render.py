import shutil,subprocess
from pathlib import Path

def render_video(scene_paths,audio_path,out_path,duration=45):
    ffmpeg=shutil.which('ffmpeg')
    if not ffmpeg: raise RuntimeError('FFmpeg is required.')
    out_path=Path(out_path); out_path.parent.mkdir(parents=True,exist_ok=True); concat=out_path.parent/'scenes.txt'; per=max(1,duration/len(scene_paths))
    concat.write_text(''.join(f"file '{Path(p).resolve()}'\nduration {per}\n" for p in scene_paths),encoding='utf-8')
    subprocess.run([ffmpeg,'-y','-f','concat','-safe','0','-i',str(concat),'-i',str(audio_path),'-vf','scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(out_path)],check=True)
    return out_path
