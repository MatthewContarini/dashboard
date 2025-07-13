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

class ChecklistComponent(Component):
    def update(self, state: State) -> None:
        self.items = state.tasks

    def render(self) -> RenderableType:
        grid = Table.grid(expand=True, padding=(0, 1))
        grid.add_column(no_wrap=True, justify="center", width=3)
        grid.add_column(ratio=1)
        for label, done in self.items:
            checkbox = Text("[X]", style="cyan") if done else Text("[ ]", style="cyan")
            grid.add_row(checkbox, Text(label))
        return Panel(
            grid,
            title=" Checklist ",
            border_style=PRIMARY_BORDER_COLOUR,
            box=box.SQUARE,
            padding=(0, 1),
        )