from typing import Dict, Any, List, Optional, Callable
from indoxagent.tools.toolkit import Toolkit
from indoxagent.utils.log import logger

try:
    from exa_py import Exa
except ImportError:
    raise ImportError("`exa_py` not installed. Please install using `pip install exa_py`")


class ExaTool(Toolkit):
    """
    ExaTool provides search functionalities using Exa, a web search engine.

    Args:
        api_key (str): Exa API key.
    """

    def __init__(self, api_key: str):
        super().__init__(name="ExaTool")  # Ensure Toolkit is initialized
        self.api_key = api_key
        self.exa = Exa(api_key=self.api_key)

        # Register functions properly
        self.register(self.search_exa)

    def search_exa(self, query: str, num_results: int = 5) -> str:
        """
        Perform a web search using Exa.

        Args:
            query (str): The search query.
            num_results (int): The number of results to return.

        Returns:
            str: Search results in JSON format.
        """
        try:
            results = self.exa.search(query=query, num_results=num_results)
            return str(results)
        except Exception as e:
            logger.error(f"Exa search failed: {e}")
            return f"Error: {e}"

    def list_functions(self):
        """Returns available tool functions."""
        return list(self.functions.keys())

