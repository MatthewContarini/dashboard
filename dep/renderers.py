from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from datetime import datetime

def render_banner() -> Align:
    ASCII_BANNER = r"""

########    ###    ########          ##     ## ########  ########  
   ##     ##   ##  ##     ##         ##     ## ##     ## ##     ## 
   ##    ##     ## ########  ####### ##     ## ########  ##     ## 
   ##    ######### ##   ##           ##     ## ##        ##     ## 
   ##    ##     ## ##     ##          #######  ##        ########  

"""
    return Align.center(Text(ASCII_BANNER, style="cyan"))

def render_time_panel(now: datetime) -> Panel:
    date_str = now.strftime("%A, %d %B %Y")
    time_str = now.strftime("%H:%M:%S")
    txt = Text(f"DATE: {date_str} | TIME: {time_str}", style="bold cyan", justify="center")
    return Panel(
        Align.center(txt),
        border_style="cyan",
        box=box.DOUBLE,
        padding=(0, 0)
    )

def render_countdown_panel(now: datetime) -> Panel:
    target = datetime(2025, 11, 1, 0, 0, 0)
    delta  = target - now
    days   = delta.days
    hours, rem    = divmod(delta.seconds, 3600)
    minutes, secs = divmod(rem, 60)

    timer_text = Text(
        f"{days}d {hours:02}:{minutes:02}:{secs:02}",
        style="bold cyan",
        justify="center",
    )
    return Panel(
        timer_text,
        title="Until Nov 1 2025",
        border_style="red",
        box=box.SQUARE,
        padding=(1,1),
    )

def render_checklist(items: list[tuple[str, bool]]) -> Panel:
    """
    items: List of (label, done_flag) tuples.
    Renders a 2-column checklist with ✔ or ✗.
    """
    grid = Table.grid(expand=True, padding=(0, 1))
    # tiny column for checkbox, then the label
    grid.add_column(no_wrap=True, justify="center", width=3)
    grid.add_column(ratio=1)

    for label, done in items:
        checkbox = Text("[X]", style="cyan") if done else Text("[ ]", style="cyan")
        grid.add_row(checkbox, Text(label))

    return Panel(
        grid,
        title=" Checklist ",
        border_style="cyan",
        box=box.SQUARE,
        padding=(0, 1),
    )

def render_news_table() -> Table:
    tbl = Table(
        title="##### RECENT EVENTS #####",
        border_style="cyan",
        box=box.SQUARE,
        expand=True
    )
    tbl.add_column("HEADLINE", style="bold cyan")
    tbl.add_column("SUMMARY", style="bright_yellow")
    tbl.add_row(
        "SYNTHETIC SOLAR BREAKTHROUGH",
        "Next-gen panels harvest energy even through city smog and acid rain."
    )
    tbl.add_row(
        "URBAN INFLATION DECELERATES",
        "Megacity markets signal stabilizing consumer power across districts."
    )
    return tbl

def render_quote_panel(quote) -> Panel:
    txt = Text(
        quote,
        style="bold bright_yellow",
        justify="center"
    )
    return Panel(
        Align.center(txt),
        padding=(1, 4),
        title="",
        border_style="cyan",
        box=box.SQUARE
    )

def render_history_panel(today_history) -> Panel:
    txt = Text(
        today_history,
        style="cyan",
        justify="center"
    )
    return Panel(
        Align.center(txt),
        padding=(1, 3),
        title="##### HISTORICAL NOTE #####",
        border_style="cyan",
        box=box.SQUARE
    )

def render_weather_details(humidity, rain_chance, rain_amount, desc):
    grid = Table.grid(expand=True, padding=(0, 0))
    grid.add_column(justify="left",  no_wrap=True)
    grid.add_column(justify="right", no_wrap=True, style="bold")

    grid.add_row("Humidity:",    f"{humidity:2d} %")
    grid.add_row("Rain Chc:", f"{rain_chance:2d} %")
    grid.add_row("Rain Amt:", f"{rain_amount:.1f} mm")
    #  → no “Conditions” row here

    # now build a Group: the grid, a blank line, then the description
    return Group(
        grid,
        Text(desc, style="bright_yellow", justify="center")
    )

def render_thermometer_panel(
    current, day_min, day_max,
    humidity, rain_chance, rain_amount,
    wind_speed, wind_dir, desc, scale_max, scale_min
) -> Panel:
    """Thermometer + weather—with the label+│+│ glued together and centered."""
    # ─ build a 2-col grid with no auto-padding
    grid = Table.grid(expand=False, padding=(0,0))
    grid.add_column(width=6, no_wrap=True)  # for " xx.x°"
    grid.add_column(width=3, no_wrap=True)  # for "│+│"

    c_round = round(current)
    min_round = round(day_min)
    max_round = round(day_max)

    for t in range(scale_max, scale_min - 1, -1):
        # ─ left label
        if t == c_round:
            lbl = Text(f"{current:5.1f}°", style="bold bright_yellow")
        elif t % 5 == 0:
            lbl = Text(f"{t:2d}°".rjust(6), style="cyan")
        else:
            lbl = Text(" " * 6)

        # ─ tube + marker
        if t == c_round:
            mark = Text("+", style="bold bright_yellow")
        elif t in (min_round, max_round):
            mark = Text("+", style="cyan")
        else:
            mark = Text(" ")
        bar = Text("│", style="cyan")
        bar.append(mark)
        bar.append("│", style="cyan")

        grid.add_row(lbl, bar)

    # ─ weather details underneath
    details = render_weather_details(
        humidity, rain_chance, rain_amount, desc
    )

    # ─ wrap them in a Group
    content = Group(grid, Text(""), details)

    # ─ center that Group within the inner content area
    centered = Align.center(content, vertical="top")

    return Panel(
        centered,
        title="Thermometer",
        border_style="cyan",
        box=box.SQUARE,
        padding=(1, 2),
        expand=False
    )

from rich.console import Group
from rich.panel   import Panel
from rich.text    import Text
from rich import box

def render_wind_compass_panel(wind_dir: str, wind_speed: float) -> Panel:
    # ─── expanded lookup for all 16 points ─────────────────────────────────────
    compass = {
        "N":   "↑",  "NNE": "↑",  "NNW": "↑",
        "NE":  "↗",  "ENE": "→",  "E":   "→",
        "ESE": "→",  "SE":  "↘",  "SSE": "↓",
        "S":   "↓",  "SSW": "↓",  "SW": "↙",
        "WSW": "←",  "W":   "←",  "WNW": "←",
        "NW":  "↖",
    }
    arrow = compass.get(wind_dir.upper(), "?")

    # ─── build the three-line compass + speed ─────────────────────────────────
    line1 = Text("+  N  +", style="cyan")
    line2 = Text.assemble(("W  ", "cyan"), (arrow, "bold red"), ("  E", "cyan"))
    line3 = Text("+  S  +", style="cyan")
    line4 = Text("")
    speed = Text(f"{wind_speed:.1f} km/h", style="bright_yellow")

    # ─── group and center ───────────────────────────────────────────────────────
    body = Group(line1, line2, line3, line4, speed)
    centered = Align(body, align="center", vertical="middle")

    return Panel(
        centered,
        title="Wind Compass",
        title_align="center",
        border_style="cyan",
        box=box.SQUARE,
        padding=(1, 1),
    )

def render_distance_panel(total_km: float) -> Panel:
    body = Align(Text(f"{total_km:.1f} km", style="bright_green"), "center", "middle")
    return Panel(body, title="Total Distance", border_style="green", box=box.SQUARE, padding=(1,1))
