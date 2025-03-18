import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from indoxagent.tools import Toolkit
from indoxagent.utils.log import logger
import arxiv

class ArxivTools(Toolkit):
    def __init__(self, search_arxiv: bool = True, read_arxiv_papers: bool = True, download_dir: Optional[Path] = None):
        """
        ArxivTools - A toolkit for searching and reading Arxiv papers.

        Args:
            search_arxiv (bool): Enables searching for Arxiv papers.
            read_arxiv_papers (bool): Enables reading and summarizing downloaded Arxiv papers.
            download_dir (Optional[Path]): Directory to save downloaded PDFs.
        """
        super().__init__(name="arxiv_tools")

        self.client: arxiv.Client = arxiv.Client()
        self.download_dir: Path = download_dir or Path(__file__).parent.joinpath("arxiv_pdfs")

        if search_arxiv:
            self.register(self.search_arxiv_and_return_articles)
        if read_arxiv_papers:
            self.register(self.read_arxiv_papers)

    def search_arxiv_and_return_articles(self, query: str, num_articles: int = 10) -> str:
        """Search Arxiv for a query and return the top articles."""
        articles = []
        logger.info(f"Searching Arxiv for: {query}")

        for result in self.client.results(
            search=arxiv.Search(
                query=query,
                max_results=num_articles,
                sort_by=arxiv.SortCriterion.Relevance,
                sort_order=arxiv.SortOrder.Descending,
            )
        ):
            try:
                article = {
                    "title": result.title,
                    "id": result.get_short_id(),
                    "entry_id": result.entry_id,
                    "authors": [author.name for author in result.authors],
                    "primary_category": result.primary_category,
                    "categories": result.categories,
                    "published": result.published.isoformat() if result.published else None,
                    "pdf_url": result.pdf_url,
                    "links": [link.href for link in result.links],
                    "summary": result.summary,
                    "comment": result.comment,
                }
                articles.append(article)
            except Exception as e:
                logger.error(f"Error processing article: {e}")
        
        return json.dumps(articles, indent=4)

    def read_arxiv_papers(self, id_list: List[str], pages_to_read: Optional[int] = None) -> str:
        """Read and summarize Arxiv papers."""
        articles = []
        logger.info(f"Fetching papers from Arxiv for: {id_list}")
        
        for result in self.client.results(search=arxiv.Search(id_list=id_list)):
            try:
                article = {
                    "title": result.title,
                    "id": result.get_short_id(),
                    "entry_id": result.entry_id,
                    "authors": [author.name for author in result.authors],
                    "primary_category": result.primary_category,
                    "categories": result.categories,
                    "published": result.published.isoformat() if result.published else None,
                    "pdf_url": result.pdf_url,
                    "links": [link.href for link in result.links],
                    "summary": result.summary,
                    "comment": result.comment,
                }

                if result.pdf_url:
                    pdf_path = result.download_pdf(dirpath=str(self.download_dir))
                    pdf_reader = PdfReader(pdf_path)
                    article["content"] = []
                    for page_number, page in enumerate(pdf_reader.pages, start=1):
                        if pages_to_read and page_number > pages_to_read:
                            break
                        content = {"page": page_number, "text": page.extract_text()}
                        article["content"].append(content)
                
                articles.append(article)
            except Exception as e:
                logger.error(f"Error processing paper: {e}")

        return json.dumps(articles, indent=4)
