from rich.console import RenderableType, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from datetime import datetime

from dashboard.components.base import Component
from dashboard.state import State
from ..config import PRIMARY_BORDER_COLOUR, PRIMARY_BOX_STYLE, PRIMARY_FONT_STYLE

class TitleComponent(Component):
    """
    Renders the ASCII banner at the top of the dashboard.
    """
    def __init__(self):
        self._banner = ""
        self._frames = [
            r"""
        ___
        /   \
        \___/

    Taringa Updater
    """,
                r"""
        ___
        /     \
        \ ___ /

    Taringa Updater
    """,
                r"""
        ___
    /       \
    \  ___  /

    Taringa Updater
    """,
                r"""
        ___
    \       /
    /  ___  \

    Taringa Updater
    """,
                r"""
        ___
        \     /
        / ___ \

    Taringa Updater
    """,
                r"""
        ___
        \   /
        /___\

    Taringa Updater
""",
        ]
        self._current_frame = 0

    def update(self, state: State) -> None:
        # Pick the current frame, then advance the index (wrap around)
        self._banner = self._frames[self._current_frame]
        self._current_frame = (self._current_frame + 1) % len(self._frames)


    def render(self) -> RenderableType:
        banner_text = Text(self._banner, style=PRIMARY_FONT_STYLE)
        # Center horizontally
        return Panel(Align(banner_text, align='center', vertical='middle'), 
                     border_style=PRIMARY_BORDER_COLOUR,
                     box=PRIMARY_BOX_STYLE)
