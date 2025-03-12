from typing import Dict, Callable


class Toolkit:
    """Base class for toolkits."""

    def __init__(self, name: str):
        self.name = name
        self.functions: Dict[str, Callable] = {}

    def register(self, function: Callable):
        """Registers a function as a tool."""
        self.functions[function.__name__] = function
