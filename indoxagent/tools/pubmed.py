import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from indoxagent.tools import Toolkit
from indoxagent.utils.log import logger
from Bio import Entrez

class PubMedTools(Toolkit):
    def __init__(self, search_pubmed: bool = True, download_papers: bool = False, email: str = None, api_key: str = None):
        """
        PubMedTools - A toolkit for searching and retrieving articles from PubMed.

        Args:
            search_pubmed (bool): Enables searching for PubMed articles.
            download_papers (bool): Enables downloading papers if applicable.
            email (str): Email address required for NCBI API compliance.
            api_key (str): Optional NCBI API key for higher request limits.
        """
        super().__init__(name="pubmed_tools")

        self.download_papers = download_papers
        
        # Set the email (NCBI requires this)
        if email is None:
            raise ValueError("An email is required to use the NCBI Entrez API.")
        Entrez.email = email

        # Set the optional API key for increased request limits
        self.api_key = api_key
        if self.api_key:
            Entrez.api_key = self.api_key  # Assign API key if provided

        if search_pubmed:
            self.register(self.search_pubmed_and_return_articles)

    def search_pubmed_and_return_articles(self, query: str, num_articles: int = 10) -> str:
        """Search PubMed for a query and return the top articles.

        Args:
            query (str): The query to search PubMed for.
            num_articles (int, optional): The number of articles to return. Defaults to 10.

        Returns:
            str: A JSON of the articles with title, authors, source, and summary.
        """
        logger.info(f"Searching PubMed for: {query}")
        
        # Perform PubMed search
        search_handle = Entrez.esearch(db="pubmed", term=query, retmax=num_articles)
        search_results = Entrez.read(search_handle)
        search_handle.close()

        # Get the list of PubMed IDs (PMID)
        pmids = search_results["IdList"]
        articles = []

        if not pmids:
            return json.dumps({"message": "No results found."}, indent=4)

        # Fetch article details based on PMIDs
        fetch_handle = Entrez.efetch(db="pubmed", id=pmids, rettype="medline", retmode="text")
        fetch_results = Entrez.read(fetch_handle)
        fetch_handle.close()

        for article in fetch_results:
            try:
                article_data = {
                    "title": article.get("TI", "No title available"),
                    "authors": article.get("AU", "No authors available"),
                    "source": article.get("SO", "No source available"),
                    "pub_date": article.get("DP", "No publication date available"),
                    "pmid": article.get("PMID", "No PMID available"),
                    "abstract": article.get("AB", "No abstract available"),
                }
                articles.append(article_data)
            except Exception as e:
                logger.error(f"Error processing article: {e}")

        return json.dumps(articles, indent=4)
