from typing import Optional, List, Dict, Any


class ModelResponse:
    """Represents a response from the model."""

    def __init__(self, content: Optional[str] = None, tool_calls: Optional[List[Dict[str, Any]]] = None):
        self.content = content
        self.tool_calls = tool_calls or []

    def to_dict(self) -> Dict[str, Any]:
        return {"content": self.content, "tool_calls": self.tool_calls}
