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

class TimeComponent(Component):
    def update(self, state: State) -> None:
        self.current_time = state.now

    def render(self) -> RenderableType:
        date_str = self.current_time.strftime("%A, %d %B %Y")
        time_str = self.current_time.strftime("%H:%M:%S")
        txt = Text(f"DATE: {date_str} | TIME: {time_str}", style="bold cyan", justify="center")
        return Panel(
            Align.center(txt),
            border_style=PRIMARY_BORDER_COLOUR,
            box=box.DOUBLE,
            padding=(0, 0)
        )