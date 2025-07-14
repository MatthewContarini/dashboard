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
    Renders a 3x3 compass rose showing where the wind is blowing.
    The center shows an arrow indicating wind direction.
    If wind speed is very low (<5 km/h), only the center dot is shown.
    """

    def update(self, state: State) -> None:
        pass

    def render(self) -> RenderableType:
        raw_dir = get_wind_dir().upper()
        speed = get_wind_speed()


        # 16-point compass: FROM direction → TO direction
        to_direction_mapping = {
            'N': 'S', 'NNE': 'SSW', 'NE': 'SW', 'ENE': 'WSW',
            'E': 'W', 'ESE': 'WNW', 'SE': 'NW', 'SSE': 'NNW',
            'S': 'N', 'SSW': 'NNE', 'SW': 'NE', 'WSW': 'ENE',
            'W': 'E', 'WNW': 'ESE', 'NW': 'SE', 'NNW': 'SSE'
        }

        # Reduce to 8 compass points that match the 3×3 grid
        grid_direction_mapping = {
            'N': 'N', 'NNE': 'N', 'NNW': 'N',
            'NE': 'NE', 'ENE': 'NE',
            'E': 'E', 'ESE': 'E',
            'SE': 'SE', 'SSE': 'S',
            'S': 'S', 'SSW': 'S',
            'SW': 'SW', 'WSW': 'SW',
            'W': 'W', 'WNW': 'W',
            'NW': 'NW', 'NNW': 'NW'
        }

        # Step 1: where is the wind going?
        to_dir_full = to_direction_mapping.get(raw_dir, None)
        compass_point = grid_direction_mapping.get(to_dir_full, None)

        # Step 2: determine arrow or dot
        if speed < 5 or compass_point is None:
            compass_point = None
            center_arrow = '·'
        else:
            center_arrow = {
                'N': '↑',
                'NE': '↗',
                'E': '→',
                'SE': '↘',
                'S': '↓',
                'SW': '↙',
                'W': '←',
                'NW': '↖',
            }.get(compass_point, '·')

        # 3x3 compass grid
        grid_labels = [
            ['NW ', 'N',  ' NE'],
            [' W',  '.',  'E'],
            ['SW ', 'S',  ' SE'],
        ]

        lines = []
                
        for row in grid_labels:
            parts = []
            for label in row:
                label_text = label        # e.g. ' W '
                clean = label.strip()     # e.g. 'W'

                if clean == '.':
                    style, disp = SECONDARY_HIGHLIGHT_FONT_STYLE, f' {center_arrow} '
                elif clean == compass_point:
                    style, disp = SECONDARY_HIGHLIGHT_FONT_STYLE, label_text
                elif clean in ["N", "E", "S", "W"]:
                    style, disp = PRIMARY_FONT_STYLE, label_text
                else:
                    style, disp = SUBTLE_HIGHLIGHT_FONT_STYLE, label_text

                parts.append(Text(disp, style=style))
            lines.append(Text.assemble(*parts))


        speed_text = Text(f"{speed:.1f} km/h", style=SECONDARY_HIGHLIGHT_FONT_STYLE)
        lines.append(Text())
        lines.append(speed_text)

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
