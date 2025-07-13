from rich.console import RenderableType, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from datetime import datetime

from dashboard.components.base import Component
from dashboard.state import State

class InputOverlayComponent(Component):
    def update(self, state: State) -> None:
        self.command_mode = getattr(state, "command_mode", False)
        self.command_buf  = getattr(state, "command_buf", "")
        self.is_entry_mode = state.in_input
        self.entry_buffer  = state.input_buf
        self.is_dist_mode  = state.dist_mode
        self.dist_buffer   = state.dist_buf

    def render(self) -> RenderableType:
        if self.command_mode:
            text = Text(f" COMMAND: {self.command_buf}", style="bold white on blue", justify="center")
            return Panel(text, box=box.SQUARE, padding=(0,1), border_style="blue")
        if self.is_entry_mode:
            text = Text(f" ENTRY: {self.entry_buffer}", style="bold white on red", justify="center")
            return Panel(text, box=box.SQUARE, padding=(0,1), border_style="red")
        if self.is_dist_mode:
            text = Text(f" DIST: {self.dist_buffer}", style="bold black on bright_green", justify="center")
            return Panel(text, box=box.SQUARE, padding=(0,1), border_style="green")
        return Panel(Text(""), box=box.SQUARE, padding=(0,1))
