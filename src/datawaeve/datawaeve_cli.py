import os
import re
from urllib.parse import urlparse
from langchain.text_splitter import TokenTextSplitter
from datasources.wikipedia_source import WikipediaSource
from langchain.text_splitter import TokenTextSplitter
from datasources.pdf_source import PDFSource
from databases.qdrant_db import QdrantDatabase
from embeddings.embedding_provider_factory import EmbeddingProviderFactory

# DataWaeve CLI class
class DataWeaveCLI:
    def __init__(self, config):
        self.config = config
        self.sources = []

    def process_sources(self):
        for source in self.sources:
            source.load_data()
            text = source.get_text()
            text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=0)
            chunks = text_splitter.split_text(text)
            provider = EmbeddingProviderFactory.get_embedding_provider(self.config)
            self.db = QdrantDatabase(self.config, provider.embeddings)
            self.db.store(chunks)

    def load_pdf_sources(self, pdf_paths):
      for pdf_path in pdf_paths:
          if os.path.isfile(pdf_path) and pdf_path.endswith('.pdf'):
              self.sources.append(PDFSource(pdf_path))
          elif os.path.isdir(pdf_path):
              pdf_files = [f for f in os.listdir(pdf_path) if f.endswith('.pdf')]
              if pdf_files:
                  self.sources.append(PDFSource(pdf_path))
              else:
                  print(f"No PDF files found in directory: {pdf_path}")
          else:
              print(f"Invalid path or unsupported format: {pdf_path}")

    def __is_valid_wikipedia_url(self, url):
        # Check if the string is a valid URL
        try:
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                return False
        except ValueError:
            return False

        # Define the Wikipedia URL pattern
        wikipedia_pattern = r'^(https?://)?(www\.)?(wikipedia\.org|[\w\-]+\.wikipedia\.org)/wiki/.+$'

        # Use regex to check if the URL matches the Wikipedia pattern
        if re.match(wikipedia_pattern, url):
            return True
        return False

    def load_wikipedia_sources(self, wikipedia_urls):
      for wikipedia_url in wikipedia_urls:
          if self.__is_valid_wikipedia_url(wikipedia_url):
              self.sources.append(WikipediaSource(wikipedia_url))
          else:
              print(f"Invalid Wikipedia URL: {wikipedia_url}")
