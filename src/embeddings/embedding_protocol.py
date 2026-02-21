# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from core import chatterpy_config
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.embeddings import Embeddings


class EmbeddingProtocol:
    def __init__(self, model_name: str, embeddings: Embeddings) -> None:
        self.model_name = model_name
        self.embeddings = embeddings


class OllamaEmbeddingProtocol(EmbeddingProtocol):
    def __init__(self) -> None:
        model_name: str = chatterpy_config.rag.embedding_model
        api_url: str = chatterpy_config.protocol.api_url
        super().__init__(model_name=model_name, embeddings=OllamaEmbeddings(model=model_name, base_url=api_url))
