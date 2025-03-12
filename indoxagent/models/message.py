from typing import Optional, Dict, Any


class Message:
    """Represents a single message in the conversation."""

    def __init__(self, role: str, content: str, name: Optional[str] = None):
        self.role = role
        self.content = content
        self.name = name

    def to_dict(self) -> Dict[str, Any]:
        """Converts message to a dictionary."""
        return {"role": self.role, "content": self.content, "name": self.name}
