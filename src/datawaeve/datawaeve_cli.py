# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
import os
import re
from urllib.parse import urlparse
from typing import List
from langchain.text_splitter import TokenTextSplitter
from databases.qdrant_db import QdrantDatabase
from datasources.pdf_source import PDFSource
from datasources.wikipedia_source import WikipediaSource
from embeddings.embedding_provider_factory import EmbeddingProviderFactory
from datasources.data_source import Source


# DataWaeve CLI class
class DataWeaveCLI:
    """
    CLI class to load PDF and Wikipedia data sources into a vector store for RAG.
    """

    def __init__(self, config):
        self.config = config
        self.sources: List[Source] = []

    def process_sources(self):
        """
        Load data from all sources, split into chunks, compute embeddings and store in DB.
        """
        provider = EmbeddingProviderFactory.get_embedding_provider(self.config)
        self.db = QdrantDatabase(self.config, provider.embeddings)
        for source in self.sources:
            source.load_data()
            text = source.get_text()
            if not text:
                print(f"[Warning] No text loaded from source: {source}")
                continue

            text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=0)
            chunks = text_splitter.split_text(text)
            self.db.store(chunks)

    def load_pdf_sources(self, pdf_paths):
        """
        Validate and add PDF sources (file or directory) to the source list.
        """
        for pdf_path in pdf_paths:
            if os.path.isfile(pdf_path) and pdf_path.endswith(".pdf"):
                self.sources.append(PDFSource(pdf_path))
            elif os.path.isdir(pdf_path):
                pdf_files = [f for f in os.listdir(pdf_path) if f.endswith(".pdf")]
                if pdf_files:
                    self.sources.append(PDFSource(pdf_path))
                else:
                    print(f"No PDF files found in directory: {pdf_path}")
            else:
                print(f"Invalid path or unsupported format: {pdf_path}")

    def __is_valid_wikipedia_url(self, url):
        """
        Validate if the given URL is a valid Wikipedia article URL.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if valid Wikipedia URL, else False.
        """
        # Check if the string is a valid URL
        try:
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                return False
        except ValueError:
            return False

        # Define the Wikipedia URL pattern
        wikipedia_pattern = r"^(https?://)?(www\.)?(wikipedia\.org|[\w\-]+\.wikipedia\.org)/wiki/.+$"

        # Use regex to check if the URL matches the Wikipedia pattern
        return re.match(wikipedia_pattern, url) is not None

    def load_wikipedia_sources(self, wikipedia_urls):
        """
        Validate and add Wikipedia sources to the source list.

        Args:
            wikipedia_urls (List[str]): List of Wikipedia URLs to add.
        """
        for wikipedia_url in wikipedia_urls:
            if self.__is_valid_wikipedia_url(wikipedia_url):
                self.sources.append(WikipediaSource(wikipedia_url))
            else:
                print(f"Invalid Wikipedia URL: {wikipedia_url}")
