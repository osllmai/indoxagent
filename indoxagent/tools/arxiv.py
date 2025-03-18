from typing import Dict, Any, List, Optional, Callable
from indoxagent.tools.toolkit import Toolkit
from indoxagent.utils.log import logger
import json

try:
    import indoxagent.tools.arxiv as arxiv
except ImportError:
    raise ImportError("`arxiv` library not installed. Please install using `pip install arxiv`")


class ArxivTool(Toolkit):
    """
    ArxivTool is designed to search for academic papers from arXiv.org based on a given query.
    It retrieves papers with their titles, abstracts, and URLs, making them accessible for further processing
    or summarization by AI models.

    Args:
        max_results (int): The maximum number of papers to fetch.
    """

    def __init__(self, max_results: int = 3):
        super().__init__(name="ArxivTool")  # Ensure Toolkit is initialized
        self.max_results = max_results
        self.register(self.search_papers)

    def search_papers(self, query: str) -> str:
        """Search for papers on arXiv based on the given query.

        Args:
            query (str): The search query for academic papers.

        Returns:
            str: A JSON string containing the list of papers found.
        """
        if not query:
            return json.dumps({"error": "No query provided"})

        search = arxiv.Search(
            query=query,
            max_results=self.max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        papers = []
        for result in search.results():
            papers.append({
                "title": result.title,
                "summary": result.summary,
                "url": result.entry_id
            })
        
        logger.info(f"Fetched {len(papers)} papers for query: {query}")
        return json.dumps(papers)