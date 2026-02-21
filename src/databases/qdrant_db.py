# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import os
from collections.abc import Iterable

from core import DistanceFunction, LoggerManager, chatterpy_config
from databases.db import Database
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

DEFAULT_QDRANT_PATH = "~/.qdrant"
DEFAULT_QDRANT_COLLECTION = "mycollection"
DEFAULT_RAG_TOP_K_CHUNKS = 10


class QdrantDatabase(Database):
    def __init__(self, embeddings) -> None:
        self._logger = LoggerManager.get_logger(name=self.__class__.__name__)
        self._qdrant_path = os.path.expanduser(chatterpy_config.rag.qdrant_path)
        self._qdrant_collection = chatterpy_config.rag.qdrant_collection

        # Verify if the path exists
        if not os.path.exists(path=self._qdrant_path):
            # If the path doesn't exist, create it
            os.makedirs(name=self._qdrant_path)
            self._logger.info(f"Created the folder: {self._qdrant_path}")
        elif not os.path.isdir(s=self._qdrant_path):
            # If the path exist but t's not a directory raise an error
            raise NotADirectoryError(f"{self._qdrant_path} exists but is not a directory.")
        else:
            # If the path exists and it is a directory
            self._logger.info(f"Qdrant directory already exists: {self._qdrant_path}")

        self._qdrant_client: QdrantClient | None = QdrantClient(path=self._qdrant_path)
        self._embeddings = embeddings
        # Check if the collection already exists in the QDrant path
        try:
            self._qdrant_client.get_collection(collection_name=self._qdrant_collection)
            self._logger.info(f"Qdrant collection {self._qdrant_collection} already exists.")
        except ValueError:
            self._logger.info(f"Qdrant collection {self._qdrant_collection} does not exist. Creating the collection...")
            embedding_vector_size: int = chatterpy_config.rag.embedding_vector_size
            embedding_distance_function: DistanceFunction = chatterpy_config.rag.embedding_distance_function
            self._qdrant_client.create_collection(
                collection_name=self._qdrant_collection,
                vectors_config=VectorParams(size=embedding_vector_size, distance=Distance(embedding_distance_function)),
            )
            self._logger.info(f"Collection {self._qdrant_collection} created.")
        self._qdrant_vectore_store = QdrantVectorStore(
            client=self._qdrant_client, collection_name=self._qdrant_collection, embedding=embeddings
        )

    def store(self, chunks: Iterable[str]) -> None:
        if chunks:
            self._qdrant_vectore_store.add_texts(texts=chunks)

    def get_context(self, user_message: str) -> list[str] | None:
        """
        Retrieve relevant context chunks for a user message.

        Args:
            user_message: The user's question/message

        Returns:
            List of relevant text chunks or None if no results
        """
        context: list[str] | None = None
        rag_top_k_chunks: int = chatterpy_config.rag.top_k_chunks
        if self._qdrant_vectore_store:
            context = [
                c.page_content
                for c in self._qdrant_vectore_store.similarity_search(query=user_message, k=rag_top_k_chunks)
            ]
        return context

    def close(self) -> None:
        """Close the Qdrant client connection gracefully."""
        if self._qdrant_client:
            try:
                self._qdrant_client.close()
                self._qdrant_client = None
            except Exception:
                self._logger.exception("Error during Qdrant client cleanup")
                pass

    def __del__(self) -> None:
        """
        Cleanup when object is destroyed.

        Note: This may be called during Python shutdown when some modules
        are already deallocated. The close() method handles this gracefully.
        """
        try:
            self.close()
        except Exception:
            self._logger.exception("Error during Qdrant client cleanup")
            pass
