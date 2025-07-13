import csv
import random
from datetime import datetime
from pathlib import Path

from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

from dashboard.components.base import Component
from dashboard.state import State
from ..config import PRIMARY_BORDER_COLOUR, PRIMARY_FONT_STYLE, \
    SECONDARY_HIGHLIGHT_FONT_STYLE, SUBTLE_HIGHLIGHT_FONT_STYLE, \
    PRIMARY_BOX_STYLE


class OTDComponent(Component):
    def __init__(self):
        # CSV at src/dashboard/data/on_this_day.csv
        data_path = (Path(__file__).parent.parent / "data" / "on_this_day.csv").resolve()
        # Now facts_by_date maps "DD-MM" → list of (year, fact) tuples
        self.facts_by_date = self._load_history_csv(data_path)
        self.quote = ""

    @staticmethod
    def _load_history_csv(path: Path) -> dict[str, list[tuple[str, str]]]:
        """
        Load the CSV and return a mapping from DD-MM to a list of (YYYY, fact).
        """
        facts: dict[str, list[tuple[str, str]]] = {}
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                full_date = row["date"].strip()      # e.g. "01-08-1995"
                fact      = row["fact"].strip()
                if not full_date or not fact:
                    continue

                # split into day, month, year
                day, month, year = full_date.split("-", 2)
                key = f"{day}-{month}"              # e.g. "01-08"

                facts.setdefault(key, []).append((year, fact))
        return facts

    def update(self, state: State) -> None:
        # Build today's key as DD-MM (ignoring the cronological year)
        today_key = state.now.strftime("%d-%m")
        choices  = self.facts_by_date.get(today_key)
        if choices:
            year, fact = random.choice(choices)
            # show year and fact
            self.quote = f"[{year}] {fact}"
        else:
            self.quote = "No On-This-Day fact available."

    def render(self) -> RenderableType:
        txt = Text(
            self.quote,
            style=SECONDARY_HIGHLIGHT_FONT_STYLE,
            justify="center",
            no_wrap=False,
        )
        # center both horizontally and vertically
        aligned = Align(txt, align="center", vertical="middle")

        return Panel(
            aligned,
            padding=(0, 4),
            title="On This Day",
            expand=True,
            border_style=PRIMARY_BORDER_COLOUR,
            box=box.MINIMAL,
        )
