import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from indoxagent.tools import Toolkit
from indoxagent.utils.log import logger
from scholarly import scholarly  # Using the scholarly package for Google Scholar API


class GoogleScholarTools(Toolkit):
    def __init__(self, search_google_scholar: bool = True, download_papers: bool = False, download_dir: Optional[Path] = None):
        super().__init__(name="google_scholar_tools")

        self.download_dir: Path = download_dir or Path(__file__).parent.joinpath("scholar_pdfs")
        self.download_papers = download_papers

        if search_google_scholar:
            self.register(self.search_google_scholar_and_return_articles)
        if download_papers:
            self.register(self.download_google_scholar_papers)

    def search_google_scholar_and_return_articles(self, query: str, num_articles: int = 10) -> str:
        """Use this function to search Google Scholar for a query and return the top articles.

        Args:
            query (str): The query to search Google Scholar for.
            num_articles (int, optional): The number of articles to return. Defaults to 10.

        Returns:
            str: A JSON string containing articles' details.
        """
        articles = []
        logger.info(f"Searching Google Scholar for: {query}")
        search_query = scholarly.search_pubs(query)

        for i, result in enumerate(search_query):
            if i >= num_articles:
                break
            try:
                article = {
                    "title": result['bib']['title'],
                    "author": result['bib']['author'],
                    "source": result['bib']['source'],
                    "url": result['url'],
                    "abstract": result['bib'].get('abstract', ''),
                    "citations": result.get('num_citations', 0),
                    "year": result['bib'].get('pub_year', ''),
                }
                articles.append(article)
            except Exception as e:
                logger.error(f"Error processing article: {e}")
        
        return json.dumps(articles, indent=4)

    def download_google_scholar_papers(self, urls: List[str]) -> str:
        """Downloads the Google Scholar papers using the provided URLs.

        Args:
            urls (list): The list of URLs for the papers.

        Returns:
            str: A confirmation message for each paper downloaded.
        """
        # Simulating paper download functionality (actual download depends on available tools and permissions)
        # This can be enhanced by utilizing specific tools for scraping Google Scholar pages or interacting with specific APIs.
        downloads = []
        for url in urls:
            # Simulating the download process. In practice, you'd need to handle the download properly.
            try:
                download_message = f"Simulated download for {url}."
                downloads.append(download_message)
            except Exception as e:
                logger.error(f"Error downloading paper: {e}")
                downloads.append(f"Failed to download {url}: {e}")

        return json.dumps(downloads, indent=4)
