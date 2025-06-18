# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from typing import Optional, List
from databases.qdrant_db import QdrantDatabase
from embeddings.embedding_provider_factory import EmbeddingProviderFactory

DEFAULT_RAG_ENABLED = False


class RAG:
    def __init__(self, config):
        """
        Initialize RAG subsystem.
        If RAG is enabled in the config, initialize the Qdrant vector database.
        """
        self.config = config
        # Convert rag_enabled config to boolean (accept string "true"/"false" or boolean)
        raw_enabled = self.config.get("rag_enabled", DEFAULT_RAG_ENABLED)
        self.rag_enabled: bool = (
            str(raw_enabled).lower() == "true" if isinstance(raw_enabled, str) else bool(raw_enabled)
        )
        if self.rag_enabled:
            embedding_provider = EmbeddingProviderFactory.get_embedding_provider(config)
            self.db: Optional[QdrantDatabase] = QdrantDatabase(self.config, embedding_provider.embeddings)
        else:
            self.db = None

    def is_enabled(self) -> bool:
        """
        Returns True if RAG is enabled, False otherwise.
        """
        return self.rag_enabled

    def get_context(self, user_message: str) -> Optional[List[str]]:
        if self.rag_enabled and self.db is not None:
            return self.db.get_context(user_message)
        return None
