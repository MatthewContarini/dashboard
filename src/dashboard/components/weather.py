from rich.console import RenderableType, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from datetime import datetime
from ..utils.display_utils import get_flashing_border

from dashboard.components.base import Component
from dashboard.state import State

from ..config import PRIMARY_BOX_STYLE, PRIMARY_FONT_STYLE, SECONDARY_HIGHLIGHT_FONT_STYLE

class WeatherDetailsComponent(Component):
    """
    Renders humidity, rain chance/amount, and description,
    centered in its panel both horizontally and vertically.
    """
    def update(self, state: State) -> None:
        pass

    def render(self) -> RenderableType:
        # Fetch data inside render to ensure fresh values
        from dashboard.utils.weather_api import (
            get_humidity,
            get_rain_chance,
            get_rain_amount,
            get_description,
        )
        # Build a two-column grid for numeric details
        grid = Table.grid(expand=True, padding=(0, 1))
        grid.add_column(justify="left", no_wrap=True, style=PRIMARY_FONT_STYLE)
        grid.add_column(justify="right", no_wrap=True, style=SECONDARY_HIGHLIGHT_FONT_STYLE)
        grid.add_row("Humidity:", f"{get_humidity():2d} %")
        grid.add_row("Rain Chc:", f"{get_rain_chance():2d} %")
        grid.add_row("Rain Amt:", f"{get_rain_amount():.1f} mm\n")
        
        desc_explainer = Text("Conditions:", style=PRIMARY_FONT_STYLE, justify="center")

        desc = Text(get_description(), style=SECONDARY_HIGHLIGHT_FONT_STYLE, justify="center")

        # Group grid + description and center within panel
        content = Align.center(
            Group(grid, desc_explainer, desc),
            vertical="middle"
        )

        return Panel(
            content,
            title="Weather Details",
            border_style=get_flashing_border(get_rain_chance()),
            box=PRIMARY_BOX_STYLE,
            padding=(1, 1),
            expand=True,
        )
