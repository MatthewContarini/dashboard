from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from rich.console import RenderableType

if TYPE_CHECKING:
    from dashboard.state import State


class Component(ABC):
    """
    Abstract base class for all dashboard components.
    Each component must implement `update()` to pull needed data from the state,
    and `render()` to return a Rich renderable (e.g., Panel, Table, Text).
    """

    @abstractmethod
    def update(self, state: "State") -> None:
        """
        Update the component's internal state from the global application state.
        """
        ...

    @abstractmethod
    def render(self) -> RenderableType:
        """
        Render the component to a Rich renderable (Panel, Table, etc.).
        """
        ...
