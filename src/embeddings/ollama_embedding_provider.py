# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from langchain_community.embeddings import OllamaEmbeddings
from embeddings.embedding_provider import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, config):
        model_name = config["embedding_model"]
        self.embeddings = OllamaEmbeddings(model=model_name)
