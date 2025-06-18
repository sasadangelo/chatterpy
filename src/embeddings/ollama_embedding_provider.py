# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from typing import Dict
from langchain_community.embeddings import OllamaEmbeddings
from embeddings.embedding_provider import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, config: Dict) -> None:
        model_name = config.get("embedding_model", "default-model")
        self.embeddings: OllamaEmbeddings = OllamaEmbeddings(model=model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.embeddings.embed(texts)
