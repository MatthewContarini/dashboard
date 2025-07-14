import time
import msvcrt
from datetime import datetime

from rich.live import Live
from rich.console import Console

from dashboard.state import State
from dashboard.layout import make_layout
from dashboard.components.base import Component
from dashboard.components.title import TitleComponent
from dashboard.components.thermometer import ThermometerComponent
from dashboard.components.weather import WeatherDetailsComponent
from dashboard.components.wind import WindCompassComponent
from dashboard.components.time import TimeComponent
from dashboard.components.news import NewsComponent
from dashboard.components.checklist import ChecklistComponent
from dashboard.components.countdown import CountdownComponent
from dashboard.components.otd_history import OTDComponent
from dashboard.components.distance import DistanceComponent
from dashboard.components.overlay import InputOverlayComponent
from dashboard.components.moon_phase import MoonComponent


def main():
    # Initialize global state
    state = State(
        tasks=[("This", False), ("That", True)],
        total_distance=0.0
    )

    # Build layout and console
    layout = make_layout()
    console = Console()
    live = Live(layout, console=console, screen=True, refresh_per_second=12)

    # Instantiate components
    components: dict[str, Component] = {
        # left components
        "content.sidebar_left.left_panel_1": WeatherDetailsComponent(),
        "content.sidebar_left.left_panel_2": ThermometerComponent(),
        "content.sidebar_left.left_panel_3": WindCompassComponent(),
        "content.sidebar_left.left_panel_4": MoonComponent(),

        # right components
        "content.sidebar_right.right_top": TitleComponent(),

        # middle components
        "content.middle_area.middle_panel_3": OTDComponent(),
        "content.middle_area.middle_panel_4": NewsComponent(),
        
        # top middle components
        


        # "left.wind": WindCompassComponent(),
        # "right.main.time": TimeComponent(),
        # "right.main.news": NewsComponent(),
        # "right.main.sub.sub_left": ChecklistComponent(),
        # "right.main.sub.sub_right": CountdownComponent(),
        # "right.footer.quote": QuoteComponent(),
        # "right.footer.distance": DistanceComponent(),
        # "overlay": InputOverlayComponent(),
    }


    with live:
        try:
            while True:
                # handle keystrokes
                if msvcrt.kbhit():
                    key = msvcrt.getwch()

                    # If already in command mode, buffer commands
                    if state.command_mode:
                        if key == "\r":
                            cmd = state.command_buf.strip().lower()
                            state.command_mode = False
                            state.command_buf = ""
                            # dispatch based on command
                            if cmd == "dist":
                                state.dist_mode = True
                                state.dist_buf = ""
                            elif cmd in ("check", "list"):
                                state.in_input = True
                                state.input_buf = ""
                                state.input_ends = time.time() + 5
                        elif key == "\x08":
                            state.command_buf = state.command_buf[:-1]
                        else:
                            state.command_buf += key
                    else:
                        # Colon enters command mode
                        if key == ":":
                            state.command_mode = True
                            state.command_buf = ""
                        # Allow toggles in checklist mode
                        elif state.in_input and (key.isdigit() or key == "\x08"):
                            if key == "\x08":
                                state.input_buf = state.input_buf[:-1]
                            else:
                                idx = int(key) - 1
                                if 0 <= idx < len(state.tasks):
                                    lbl, done = state.tasks[idx]
                                    state.tasks[idx] = (lbl, not done)
                                state.input_buf += key
                        # Distance entry
                        elif state.dist_mode and (key.isdigit() or key == "." or key == "\x08" or key == "\r"):
                            if key == "\r":
                                try:
                                    state.total_distance += float(state.dist_buf)
                                except ValueError:
                                    pass
                                state.dist_mode = False
                                state.dist_buf = ""
                            elif key == "\x08":
                                state.dist_buf = state.dist_buf[:-1]
                            else:
                                state.dist_buf += key

                # update timestamp
                now = datetime.now().replace(
                    second=(datetime.now().second // 5) * 5,
                    microsecond=0
                )
                state.now = now

                # exit checklist if timed out
                if state.in_input and time.time() >= state.input_ends:
                    state.in_input = False
                    state.input_buf = ""

                # render all components
                for region, comp in components.items():
                    comp.update(state)
                    node = layout
                    
                    for part in region.split('.'):
                        node = node[part]
                    node.update(comp.render())

                # # throttle update rate: fast when in any entry mode, slower otherwise
                # if state.command_mode or state.in_input or state.dist_mode:
                #     time.sleep(0.01)
                # else:
                #     time.sleep(1/100)

        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()