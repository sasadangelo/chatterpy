# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from urllib.parse import urlparse
import wikipediaapi
from datasources.data_source import Source


class WikipediaSource(Source):
    """
    Wikipedia source loader that fetches content from a Wikipedia page URL.
    """

    def __init__(self, source: str) -> None:
        """
        Initialize with a Wikipedia URL.

        Args:
            source (str): Wikipedia page URL.
        """
        self.source = source
        self.pages = []

    def extract_title_from_url(self) -> str:
        """
        Extract the Wikipedia page title from the URL.

        Returns:
            str: The Wikipedia page title.

        Raises:
            ValueError: If the URL is not a valid Wikipedia URL.
        """
        parsed_url = urlparse(self.source)
        path = parsed_url.path
        if path.startswith("/wiki/"):
            return path[len("/wiki/") :]
        else:
            raise ValueError("The URL does not seem to be a valid Wikipedia URL.")

    def load_data(self) -> None:
        """
        Load the Wikipedia page content into self.pages.
        """
        # Initialize the Wikipedia API
        user_agent = "DataWaeve CLI"
        wiki_wiki = wikipediaapi.Wikipedia(user_agent, "en")

        # Extract the page title from the URL
        try:
            title = self.extract_title_from_url()
            page = wiki_wiki.page(title)

            if not page.exists():
                print(f"Page not found: {self.source}")
                return []

            # Return the page content as a list of documents
            self.pages = [page.text]
            print(f"Loaded content from Wikipedia page: {self.source}")
        except Exception as e:
            print(f"An error occurred while loading Wikipedia data: {e}")
            self.pages = []

    def get_text(self) -> str:
        """
        Return the text content of the loaded Wikipedia page.

        Returns:
            str: The text of the Wikipedia page or empty string if no content loaded.
        """
        if self.pages:
            return self.pages[0]
        return ""
