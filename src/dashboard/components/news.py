from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from dashboard.components.base import Component
from dashboard.state import State
from ..utils.news_utils import get_top_stories
from ..config import PRIMARY_BORDER_COLOUR, PRIMARY_FONT_STYLE, \
    SECONDARY_HIGHLIGHT_FONT_STYLE, SUBTLE_HIGHLIGHT_FONT_STYLE, \
    PRIMARY_BOX_STYLE

# Ratios for columns
HEADLINE_RATIO = 1
SUMMARY_RATIO = 2

class NewsComponent(Component):
    def __init__(self) -> None:
        self.news_entries: list[dict] = []

    def update(self, state: State) -> None:
        self.news_entries = get_top_stories(
            count=4,
            exclude_categories=["Sport", "Entertainment"],
        )

    def render(self) -> RenderableType:
        # Create table that expands so ratios apply
        tbl = Table(
            show_lines=True,
            box=box.SIMPLE,
            pad_edge=False,
            border_style=PRIMARY_BORDER_COLOUR,
            expand=True,
        )
        # Only set ratio on columns; all styling via Text
        tbl.add_column("Headline", ratio=HEADLINE_RATIO, header_style=PRIMARY_FONT_STYLE)
        tbl.add_column("Summary", ratio=SUMMARY_RATIO, header_style=PRIMARY_FONT_STYLE)

        for story in self.news_entries:
            raw_headline = story.get("headline", "").strip()
            raw_summary = story.get("description", "").strip()

            # Enforce max lines + ellipsis using Text
            headline = Text(
                raw_headline,
                style=PRIMARY_FONT_STYLE,
                overflow="ellipsis",
                no_wrap=False
            )
            summary = Text(
                raw_summary,
                style=SECONDARY_HIGHLIGHT_FONT_STYLE,
                overflow="ellipsis",
                no_wrap=False,
            )

            tbl.add_row(headline, summary)

        return Panel(
            tbl,
            title="Recent Updates",
            border_style=PRIMARY_BORDER_COLOUR,
            box=box.MINIMAL,
            padding=(0, 1),
            expand=True,
        )
