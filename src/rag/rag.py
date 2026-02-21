# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from core import chatterpy_config
from databases.qdrant_db import QdrantDatabase
from embeddings import EmbeddingProtocol, EmbeddingProtocolFactory


class RAG:
    """
    RAG (Retrieval Augmented Generation) handler.

    Manages the retrieval of relevant context from the vector database
    to augment LLM responses with domain-specific knowledge.
    """

    def __init__(self) -> None:
        """Initialize RAG with configuration from config.yaml."""
        self.rag_enabled: bool = chatterpy_config.rag.enabled
        embedding_protocol: EmbeddingProtocol = EmbeddingProtocolFactory.get_embedding_protocol()
        self.db: QdrantDatabase | None = (
            QdrantDatabase(embeddings=embedding_protocol.embeddings) if self.rag_enabled else None
        )

    def is_enabled(self) -> bool:
        """Check if RAG is enabled."""
        return self.rag_enabled

    def get_context(self, user_message: str) -> list[str] | None:
        """
        Retrieve relevant context for a user message.

        Args:
            user_message: The user's question/message

        Returns:
            List of relevant text chunks or None if RAG is disabled or no results
        """
        return self.db.get_context(user_message) if self.rag_enabled and self.db else None
