from rich.console import RenderableType, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from datetime import datetime

from dashboard.components.base import Component
from dashboard.state import State
from ..config import PRIMARY_BORDER_COLOUR

class CountdownComponent(Component):
    def update(self, state: State) -> None:
        self.current_time = state.now

    def render(self) -> RenderableType:
        target = datetime(2025, 11, 1, 0, 0, 0)
        delta = target - self.current_time
        days = delta.days
        hours, rem = divmod(delta.seconds, 3600)
        minutes, secs = divmod(rem, 60)
        timer_text = Text(
            f"{days}d {hours:02}:{minutes:02}:{secs:02}",
            style="bold cyan",
            justify="center",
        )
        return Panel(
            timer_text,
            title="Until Nov 1 2025",
            border_style=PRIMARY_BORDER_COLOUR,
            box=box.SQUARE,
            padding=(1,1),
        )