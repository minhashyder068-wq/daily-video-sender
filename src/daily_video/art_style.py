from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def font(size):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','C:/Windows/Fonts/arialbd.ttf']:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def render_scene(text,index,out_dir):
    out_dir=Path(out_dir); out_dir.mkdir(parents=True,exist_ok=True)
    w,h=1080,1920; im=Image.new('RGB',(w,h),(238,225,205)); d=ImageDraw.Draw(im)
    d.ellipse((w-350,120,w-80,390),fill=(245,190,90)); d.polygon([(0,1250),(300,850),(650,1250)],fill=(120,150,125)); d.polygon([(350,1250),(760,760),(1080,1250)],fill=(95,125,110)); d.rectangle((0,1250,w,h),fill=(210,185,145))
    d.text((70,80),f'DAY • SCENE {index}',font=font(54),fill=(45,45,45))
    d.rounded_rectangle((70,1380,w-70,h-120),radius=35,fill=(250,245,235),outline=(80,70,60),width=3)
    d.text((110,1440),text[:180],font=font(42),fill=(40,40,40))
    path=out_dir/f'scene_{index:02d}.png'; im.save(path); return path
