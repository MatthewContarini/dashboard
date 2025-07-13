from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from dashboard.components.base import Component
from dashboard.state import State
from dashboard.utils.weather_api import (
    get_current_temperature,
    get_day_min_temperature,
    get_day_max_temperature,
)
from dashboard.config import SCALE_MAX_TEMP, SCALE_MIN_TEMP
from ..config import PRIMARY_BORDER_COLOUR, PRIMARY_FONT_STYLE, \
    SECONDARY_HIGHLIGHT_FONT_STYLE, SUBTLE_HIGHLIGHT_FONT_STYLE, \
    PRIMARY_BOX_STYLE

class ThermometerComponent(Component):
    def update(self, state: State) -> None:
        # No internal caching; data fetched each render
        return

    def render(self) -> RenderableType:
        # Fetch current, min, and max temperatures
        current_temperature = get_current_temperature()
        daily_min_temperature = get_day_min_temperature()
        daily_max_temperature = get_day_max_temperature()

        # Check if the daily minimum falls below the scale
        is_min_overflow = daily_min_temperature < SCALE_MIN_TEMP
        is_max_overflow = daily_max_temperature > SCALE_MAX_TEMP

        # Round values for marker positions
        rounded_min_temperature = round(daily_min_temperature)
        rounded_max_temperature = round(daily_max_temperature)
        rounded_current_temperature = round(current_temperature)

        # Build a two-column grid: labels and thermometer tube
        table_grid = Table.grid(expand=False, padding=(0, 0))
        table_grid.add_column(width=6, no_wrap=True)  # label column
        table_grid.add_column(width=3, no_wrap=True)  # tube column

        # Iterate from top of scale down to bottom
        for temperature_level in range(SCALE_MAX_TEMP, SCALE_MIN_TEMP - 1, -1):
            # Prepare the label cell
            if temperature_level == rounded_current_temperature:
                label_text = Text(f"{current_temperature:5.1f}°", style=SECONDARY_HIGHLIGHT_FONT_STYLE)
            elif is_min_overflow and temperature_level == SCALE_MIN_TEMP:
                # Show actual min temp if underflow
                label_text = Text(f"{daily_min_temperature:5.1f}°", style=SUBTLE_HIGHLIGHT_FONT_STYLE)
            elif is_max_overflow and temperature_level == SCALE_MAX_TEMP:
                # Show actual max temp if overflow
                label_text = Text(f"{daily_max_temperature:5.1f}°", style=SUBTLE_HIGHLIGHT_FONT_STYLE)              
            elif temperature_level % 5 == 0:
                label_text = Text(f"{temperature_level:2d}°".rjust(6), style=PRIMARY_FONT_STYLE)
            else:
                label_text = Text(" " * 6)

            # Prepare the thermometer tube with marker
            if temperature_level == rounded_current_temperature:
                marker_text = Text("+", style=SECONDARY_HIGHLIGHT_FONT_STYLE)
            elif is_min_overflow and temperature_level == SCALE_MIN_TEMP:
                marker_text = Text("↓", style=SUBTLE_HIGHLIGHT_FONT_STYLE)
            elif is_max_overflow and temperature_level == SCALE_MAX_TEMP:
                marker_text = Text("↑", style=SUBTLE_HIGHLIGHT_FONT_STYLE)
            elif temperature_level in (rounded_min_temperature, rounded_max_temperature):
                marker_text = Text("+", style=PRIMARY_FONT_STYLE)
            else:
                marker_text = Text(" ")
            tube_text = Text("│", style=PRIMARY_FONT_STYLE)
            tube_text.append(marker_text)
            tube_text.append("│", style=PRIMARY_FONT_STYLE)

            # Add the row to the grid
            table_grid.add_row(label_text, tube_text)

        # Wrap the grid in a panel
        return Panel(
            table_grid,
            title="Thermometer",
            border_style=PRIMARY_BORDER_COLOUR,
            padding=(1, 3),
            box=PRIMARY_BOX_STYLE,
            expand=True,
        )
