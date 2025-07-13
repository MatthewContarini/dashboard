from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple

@dataclass
class State:
    """
    Global application state.
    Stores mutable values and buffers used by components.
    """
    tasks: List[Tuple[str, bool]] = field(default_factory=list)
    in_input: bool = False
    input_buf: str = ""
    input_ends: float = 0.0
    dist_mode: bool = False
    dist_buf: str = ""
    total_distance: float = 0.0
    now: datetime = field(default_factory=datetime.now)
    command_mode: bool = False
    command_buf: str = ""