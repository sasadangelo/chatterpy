# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import os

from datasources.data_source import Source
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents.base import Document


class PDFSource(Source):
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.pages: list[Document] = []

    def load_data(self) -> None:
        if os.path.isfile(path=self.path) and self.path.endswith(".pdf"):
            loader: PyPDFLoader = PyPDFLoader(file_path=self.path)
            self.pages = loader.load()
            print(f"Loaded {len(self.pages)} pages from file: {self.path}")
        elif os.path.isdir(s=self.path):
            pdf_files: list[str] = [f for f in os.listdir(self.path) if f.endswith(".pdf")]
            if not pdf_files:
                print(f"No PDF files found in directory: {self.path}")

            for filename in pdf_files:
                filepath: str = os.path.join(self.path, filename)
                loader = PyPDFLoader(file_path=filepath)
                docs: list[Document] = loader.load()
                self.pages.extend(docs)
                print(f"Loaded {len(docs)} pages from file: {filename}")

            print(f"Total loaded documents from directory: {len(self.pages)}")
        else:
            print(f"Invalid PDF source: {self.path}")

    def get_text(self) -> str:
        if self.pages:
            page_text = ""
            for page in self.pages:
                page_text += page.page_content
            return page_text
        else:
            return ""
