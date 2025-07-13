from rich.console import RenderableType, Group
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

from dashboard.components.base import Component
from dashboard.state import State
from dashboard.utils.weather_api import get_wind_dir, get_wind_speed
from ..config import PRIMARY_BORDER_COLOUR, PRIMARY_FONT_STYLE, \
    SECONDARY_HIGHLIGHT_FONT_STYLE, SUBTLE_HIGHLIGHT_FONT_STYLE, \
    PRIMARY_BOX_STYLE

class WindCompassComponent(Component):
    """
    Renders a 3x3 compass rose with the current wind direction highlighted.
    The center dot is always highlighted. If wind speed is very low (<1 km/h),
    only the center dot is highlighted.
    """
    def update(self, state: State) -> None:
        pass

    def render(self) -> RenderableType:
        # Get raw wind data
        raw_dir = get_wind_dir().upper()
        speed = get_wind_speed()

        # Map API directions to the 8 compass points
        direction_mapping = {
            'N': 'N', 'NNE': 'N', 'NNW': 'N',
            'NE': 'NE', 'ENE': 'NE',
            'E': 'E', 'ESE': 'E',
            'SE': 'SE', 'SSE': 'S',
            'S': 'S', 'SSW': 'S',
            'SW': 'SW', 'WSW': 'SW',
            'W': 'W', 'WNW': 'W',
            'NW': 'NW', 'NNW': 'NW'
        }
        # Determine which compass point to highlight
        compass_point = direction_mapping.get(raw_dir)
        cardinal_dirs = ["N", "E", "S", "W"]
        # If very low speed, ignore direction
        if speed < 5:
            compass_point = None

        # Define the 3x3 display grid
        grid_labels = [
            ['NW ', 'N',  'NE'],
            [' W ',  '.',  'E'],
            ['SW ', 'S',  'SE'],
        ]

        # Build lines for each compass row
        lines = []
        for row in grid_labels:
            parts = []
            for label in row:
                if label == '.':
                    # center dot always highlighted
                    style = SECONDARY_HIGHLIGHT_FONT_STYLE
                    disp = ' · '
                elif label == compass_point:
                    # current wind direction highlighted
                    style = SECONDARY_HIGHLIGHT_FONT_STYLE
                    disp = f'{label.center(3)}'
                elif str.strip(label) in cardinal_dirs:
                    # cardinal directions use primary style
                    style = PRIMARY_FONT_STYLE
                    disp = f'{label.center(3)}'
                else:
                    # intercardinal points use subtle highlight
                    style = SUBTLE_HIGHLIGHT_FONT_STYLE
                    disp = f'{label.center(3)}'

                parts.append(Text(disp, style=style))
            lines.append(Text.assemble(*parts))

        # Append a line for speed value
        speed_text = Text(f"{speed:.1f} km/h", style=SECONDARY_HIGHLIGHT_FONT_STYLE)
        lines.append(Text())  # blank spacer
        lines.append(speed_text)

        # Center the group
        body = Align.center(Group(*lines), vertical='middle')

        return Panel(
            body,
            title="Wind Compass",
            title_align="center",
            border_style=PRIMARY_BORDER_COLOUR,
            box=PRIMARY_BOX_STYLE,
            padding=(1, 1),
            expand=True,
        )
