import time
from pathlib import Path
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

from dashboard.components.base import Component
from dashboard.state import State
from ..config import PRIMARY_BORDER_COLOUR, PRIMARY_BOX_STYLE, PRIMARY_FONT_STYLE

ANIMATION_FRAMES_DIR = Path(__file__).parent.parent / "animations" / "title_animation"
ANIMATION_FPS        = 50.0  # desired banner framerate

class TitleComponent(Component):
    def __init__(self):
        # load text‐frames
        self._frames = []
        if ANIMATION_FRAMES_DIR.exists():
            for p in sorted(ANIMATION_FRAMES_DIR.glob("*.txt")):
                self._frames.append(p.read_text(encoding="utf-8"))
        if not self._frames:
            self._frames = ["Taringa Updater"]

        # time‐based indexing
        self._start_time = time.monotonic()
        self._banner     = self._frames[0]

    def update(self, state: State) -> None:
        # compute how many seconds since init
        elapsed = time.monotonic() - self._start_time
        # compute which frame we *should* be on
        frame_idx = int(elapsed * ANIMATION_FPS) % len(self._frames)
        self._banner = self._frames[frame_idx]

    def render(self) -> RenderableType:
        txt = Text(self._banner, style=PRIMARY_FONT_STYLE)
        return Panel(
            Align(txt, align="center", vertical="middle"),
            border_style=PRIMARY_BORDER_COLOUR,
            box=PRIMARY_BOX_STYLE,
        )
