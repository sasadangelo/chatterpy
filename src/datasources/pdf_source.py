# Class for managing PDF data sources
import os
from datasources.data_source import Source
from langchain_community.document_loaders import PyPDFLoader

class PDFSource(Source):
    def __init__(self, source):
        self.source = source
        self.pages = []

    def load_data(self):
        if os.path.isfile(self.source) and self.source.endswith('.pdf'):
            loader = PyPDFLoader(self.source)
            self.pages = loader.load()
            print(f"Loaded {len(self.pages)} pages from file: {self.source}")
        elif os.path.isdir(self.source):
            pdf_files = [f for f in os.listdir(self.source) if f.endswith('.pdf')]
            if not pdf_files:
                print(f"No PDF files found in directory: {self.source}")

            for filename in pdf_files:
                filepath = os.path.join(self.source, filename)
                loader = PyPDFLoader(filepath)
                docs = loader.load()
                self.pages.extend(docs)
                print(f"Loaded {len(docs)} pages from file: {filename}")

            print(f"Total loaded documents from directory: {len(self.pages)}")
        else:
            print(f"Invalid PDF source: {self.source}")

    def get_text(self):
        if self.pages:
            page_text = ""
            for page in self.pages:
                page_text += page.page_content
            return page_text
        else:
            return ""
