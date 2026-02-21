# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import os
import re
from typing import Any
from urllib.parse import ParseResult, urlparse

from core import LoggerManager, chatterpy_config
from databases.qdrant_db import QdrantDatabase
from datasources.data_source import Source
from datasources.pdf_source import PDFSource
from datasources.wikipedia_source import WikipediaSource
from embeddings import EmbeddingProtocol, EmbeddingProtocolFactory
from langchain_text_splitters import TokenTextSplitter

DEFAULT_CHUNK_SIZE = 100
DEFAULT_CHUNK_OVERLAP = 0


# DataWaeve CLI class
class DataWeaveCLI:
    def __init__(self) -> None:
        self._logger = LoggerManager.get_logger(name=self.__class__.__name__)
        self.sources: list[Source] = []

    def process_sources(self) -> None:
        for source in self.sources:
            source.load_data()
            text: str = source.get_text()
            chunk_size: int = chatterpy_config.rag.document_chunk_size
            chunk_overlap: int = chatterpy_config.rag.document_chunk_overlap
            text_splitter: TokenTextSplitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            chunks: list[str] = text_splitter.split_text(text)
            embedding_protocol: EmbeddingProtocol = EmbeddingProtocolFactory.get_embedding_protocol()
            self.db = QdrantDatabase(embeddings=embedding_protocol.embeddings)
            self.db.store(chunks)

    def load_pdf_sources(self, pdf_paths) -> None:
        for pdf_path in pdf_paths:
            if os.path.isfile(path=pdf_path) and pdf_path.endswith(".pdf"):
                self.sources.append(PDFSource(path=pdf_path))
            elif os.path.isdir(s=pdf_path):
                pdf_files = [f for f in os.listdir(pdf_path) if f.endswith(".pdf")]
                if pdf_files:
                    self.sources.append(PDFSource(path=pdf_path))
                else:
                    print(f"No PDF files found in directory: {pdf_path}")
            else:
                print(f"Invalid path or unsupported format: {pdf_path}")

    def __is_valid_wikipedia_url(self, url) -> bool:
        # Check if the string is a valid URL
        try:
            parsed_url: Any | ParseResult = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                return False
        except ValueError:
            return False

        # Define the Wikipedia URL pattern
        wikipedia_pattern = r"^(https?://)?(www\.)?(wikipedia\.org|[\w\-]+\.wikipedia\.org)/wiki/.+$"

        # Use regex to check if the URL matches the Wikipedia pattern
        if re.match(wikipedia_pattern, url):
            return True
        return False

    def load_wikipedia_sources(self, wikipedia_urls) -> None:
        for wikipedia_url in wikipedia_urls:
            if self.__is_valid_wikipedia_url(url=wikipedia_url):
                self.sources.append(WikipediaSource(source=wikipedia_url))
            else:
                print(f"Invalid Wikipedia URL: {wikipedia_url}")
