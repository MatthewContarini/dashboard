import time
from ..config import PRIMARY_BORDER_COLOUR, PRIMARY_HIGHLIGHT_BORDER_STYLE

FLASH_INTERVAL = 2.0

def get_flashing_border(chance_of_rain: int) -> str:
    if chance_of_rain > 80:
        phase = int(time.time() / FLASH_INTERVAL) % 2
        return PRIMARY_HIGHLIGHT_BORDER_STYLE if phase == 0 else PRIMARY_BORDER_COLOUR
    return PRIMARY_BORDER_COLOUR