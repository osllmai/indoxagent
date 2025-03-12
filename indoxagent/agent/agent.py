from typing import List, Optional, Dict, Any
from indoxagent.models.message import Message
from indoxagent.models.response import ModelResponse
from indoxagent.tools.toolkit import Toolkit
from indoxagent.utils.log import logger


class Agent:
    """
    Main Agent class for handling messages, executing tools, and managing responses.
    """

    def __init__(self, model, tools: Optional[List[Toolkit]] = None):
        self.model = model
        self.tools = tools or []

        # Debugging: Print registered tools
        logger.info(f"Initializing Agent with tools: {[tool.name for tool in self.tools]}")

        # Ensure tool functions are properly registered
        self.tool_registry = {}
        for toolkit in self.tools:
            if hasattr(toolkit, "functions"):  # Ensure `functions` exists
                for func_name, func in toolkit.functions.items():
                    self.tool_registry[func_name] = func

        logger.info(f"Tool Registry: {list(self.tool_registry.keys())}")  # Debugging

    def invoke(self, messages: List[Message]) -> ModelResponse:
        """
        Process a conversation using the model and return the response.

        Args:
            messages (List[Message]): Conversation messages.

        Returns:
            ModelResponse: The processed response.
        """
        logger.info("Invoking model...")
        response = self.model.invoke(messages)
        return self._process_response(response)

    async def ainvoke(self, messages: List[Message]) -> ModelResponse:
        """
        Asynchronous version of invoke.

        Args:
            messages (List[Message]): Conversation messages.

        Returns:
            ModelResponse: The processed response.
        """
        logger.info("Async invoking model...")
        response = await self.model.ainvoke(messages)
        return self._process_response(response)

    def _process_response(self, response: ModelResponse) -> ModelResponse:
        """
        Process the model response, executing tools if necessary.

        Args:
            response (ModelResponse): The model response.

        Returns:
            ModelResponse: Final processed response.
        """
        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call.get("function", {}).get("name")
                tool_args = tool_call.get("function", {}).get("arguments", {})

                if tool_name in self.tool_registry:
                    tool_function = self.tool_registry[tool_name]
                    logger.info(f"Executing tool: {tool_name} with args {tool_args}")
                    tool_output = tool_function(**tool_args)  # Direct function call
                    response.content += f"\n\nTool [{tool_name}] output: {tool_output}"
                else:
                    logger.warning(f"Tool {tool_name} not found!")

        return response
