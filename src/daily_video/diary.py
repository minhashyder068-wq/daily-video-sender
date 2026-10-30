from pathlib import Path

def load_diary(path='input/today.md'):
    text=Path(path).read_text(encoding='utf-8').strip()
    if not text: raise ValueError('Diary input is empty.')
    return ' '.join(x.strip() for x in text.splitlines() if x.strip() and not x.startswith('#'))

def make_scenes(text, max_scenes=6):
    parts=[x.strip() for x in text.split('.') if x.strip()]
    return parts[:max_scenes] or [text]
