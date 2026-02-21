# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from urllib.parse import ParseResult, urlparse

import wikipediaapi
from datasources.data_source import Source
from wikipediaapi import Wikipedia, WikipediaPage


class WikipediaSource(Source):
    def __init__(self, source) -> None:
        self.source = source
        self.pages: list[str] = []

    def extract_title_from_url(self) -> str:
        # Extract the page title from the Wikipedia URL
        parsed_url: ParseResult = urlparse(url=self.source)
        path: str = parsed_url.path
        if path.startswith("/wiki/"):
            return path[len("/wiki/") :]
        else:
            raise ValueError("The URL does not seem to be a valid Wikipedia URL.")

    def load_data(self) -> None:
        # Initialize the Wikipedia API
        user_agent = "DataWaeve CLI"
        wiki_wiki: Wikipedia = wikipediaapi.Wikipedia(user_agent=user_agent, language="en")

        # Extract the page title from the URL
        try:
            title: str = self.extract_title_from_url()
            page: WikipediaPage = wiki_wiki.page(title)

            if not page.exists():
                print(f"Page not found: {self.source}")
                return

            # Return the page content as a list of documents
            self.pages = [page.text]
            print(f"Loaded content from Wikipedia page: {self.source}")
        except Exception as e:
            print(f"An error occurred while loading Wikipedia data: {e}")

    def get_text(self) -> str:
        if self.pages:
            return self.pages[0]
        else:
            return ""
