"""Fuente HTTP agregada para regresiones históricas de texto."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def runtime_http_source() -> str:
    paths = (
        ROOT / 'app' / 'main.py',
        ROOT / 'app' / 'portals' / 'asegurado' / 'router.py',
        ROOT / 'app' / 'portals' / 'developer' / 'router.py',
    )
    parts = []
    for path in paths:
        text = path.read_text(encoding='utf-8')
        if path.name == 'router.py':
            text = text.replace('@router.', '@app.')
        parts.append(text)
    return '\n\n'.join(parts)
