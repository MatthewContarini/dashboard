from rich.console import RenderableType, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from dashboard.components.base import Component
from dashboard.state import State
from dashboard.utils.weather_api import get_moon_phase

from ..config import PRIMARY_BORDER_COLOUR, PRIMARY_FONT_STYLE, \
    SECONDARY_HIGHLIGHT_FONT_STYLE, SUBTLE_HIGHLIGHT_FONT_STYLE, \
    PRIMARY_BOX_STYLE

# Multi-line ASCII art for each lunar phase 
PHASE_ASCII = {
    "New Moon": r"""
       _..._     
     .'     `.    
    :         :
    :         :  
    `.       .'  
      `-...-'  
""",
    "Waxing Crescent": r"""
       _..._     
     .::'   `.    
    :::       :  
    :::       :  
    `::.     .'  
      `':..-'   
""",
    "First Quarter": r"""
       _..._     
     .::::  `.    
    ::::::    : 
    ::::::    :  
    `:::::   .'  
      `'::.-'  
""",
    "Waxing Gibbous": r"""
       _..._     
     .::::. `.    
    :::::::.  : 
    ::::::::  :  
    `::::::' .'  
      `'::'-' 
""",
    "Full Moon": r"""
       _..._     
     .:::::::.    
    :::::::::::
    ::::::::::: 
    `:::::::::'  
      `':::'' 
""",
    "Waning Gibbous": r"""
       _..._     
     .' .::::.    
    :  ::::::::
    :  ::::::::  
    `. '::::::'  
      `-.::'' 
""",
    "Last Quarter": r"""
       _..._   
     .'  ::::. 
    :    ::::::
    :    ::::::
    `.   :::::'
      `-.::''  
""",
    "Waning Crescent": r"""
       _..._     
     .'   `::.    
    :       :::  
    :       :::  
    `.     .::'  
      `-..:''  
""",
}

class MoonComponent(Component):
    """
    Renders the current Moon phase as ASCII art (centered automatically)
    with the phase name underneath, and a flashing border on Full Moon.
    """
    def __init__(self) -> None:
        self.phase = get_moon_phase()

    def update(self, state: State) -> None:
        self.phase = get_moon_phase()

    def render(self) -> RenderableType:
        # convert to list
        art_lines = PHASE_ASCII[self.phase].splitlines()
        # strip white space
        art_lines = [line.strip() for line in art_lines]

        # One-column grid: expands to fill panel and centers each row
        grid = Table.grid(expand=True, padding=(0, 0))
        grid.add_column(justify="center")

        # Add each ASCII-art line
        for line in art_lines:
            grid.add_row(line, style=SECONDARY_HIGHLIGHT_FONT_STYLE)
        # Spacer row
        grid.add_row("")
        # Phase name row
        grid.add_row(f"{self.phase}", style=PRIMARY_FONT_STYLE)

        return Panel(
            grid,
            title=" Moon Phase ",
            border_style=PRIMARY_BORDER_COLOUR,
            box=PRIMARY_BOX_STYLE,
            padding=(0, 0),
            expand=True
        )
