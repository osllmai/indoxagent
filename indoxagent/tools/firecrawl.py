from typing import Dict, Any, List, Optional, Callable
from indoxagent.tools.toolkit import Toolkit
from indoxagent.utils.log import logger
import json

try:
    from firecrawl import FirecrawlApp
except ImportError:
    raise ImportError("`firecrawl-py` not installed. Please install using `pip install firecrawl-py`")


class FirecrawlTools(Toolkit):
    """
    Firecrawl is a web crawling and scraping tool designed to convert entire websites
    into Large Language Model (LLM)-ready data, such as clean markdown or structured
    formats. It efficiently handles tasks like scraping, crawling, and data extraction,
    making it particularly useful for AI applications that require structured web data.

    Args:
        api_key (str): firecrawl API key.
        Scrape (bool): Retrieve content from a specific URL in LLM-ready formats 
        Crawl (bool): Navigate through all accessible subpages of a website, 
                      extracting clean data without the need for a sitemap.
    """

    def __init__(self, api_key: str, crawl: bool, scrape: bool):
        super().__init__(name="FirecrawlTool")  # Ensure Toolkit is initialized
        self.api_key = api_key
        self.app = FirecrawlApp(api_key=self.api_key)

        if crawl:
            scrape = False
        elif not scrape:
            crawl = True

        # Register functions properly
        if scrape:
            self.register(self.scrape_website)
        if crawl:
            self.register(self.crawl_website)

    def scrape_website(self, url: str) -> str:
        """Perform website scraping using Firecrawl.

        Args:
            url (str): The URL that needs to be scraped.

        Returns:
            Results of the scraping in JSON format.
        """

        if url is None:
            return "No URL provided"

        results = self.app.scrape_url(url)
        return json.dumps(results)
    


    def crawl_website(self, url: str) -> str:
        """Perform website crawling using Firecrawl.

        Args:
            url (str): The URL that needs to be crawled.

        Returns:
            Results of the crawling in JSON format.
        """
        if url is None:
            return "No URL provided"

        results = self.app.crawl_url(url)
        return json.dumps(results)