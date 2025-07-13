from rich.console import RenderableType, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from datetime import datetime
from ..config import PRIMARY_BORDER_COLOUR

from dashboard.components.base import Component
from dashboard.state import State

class DistanceComponent(Component):
    def update(self, state: State) -> None:
        self.total_distance = state.total_distance

    def render(self) -> RenderableType:
        txt = Text(f"{self.total_distance:.1f} km", style="bright_green", justify="center")
        return Panel(
            Align.center(txt, vertical="middle"),
            title="Total Distance",
            border_style=PRIMARY_BORDER_COLOUR,
            box=box.SQUARE,
            padding=(1,1)
        )