# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from core import chatterpy_config
from embeddings.embedding_protocol import EmbeddingProtocol, OllamaEmbeddingProtocol


class EmbeddingProtocolFactory:
    protocols: dict[str, type[OllamaEmbeddingProtocol]] = {
        "ollama": OllamaEmbeddingProtocol,
    }

    # The single provider instance
    _instance: EmbeddingProtocol | None = None

    @classmethod
    def get_embedding_protocol(cls) -> EmbeddingProtocol:
        # If the instance already exists, return it
        if cls._instance is not None:
            return cls._instance

        # Otherwise, create it
        protocol_name: str = chatterpy_config.rag.embedding_protocol
        protocol_class: type[OllamaEmbeddingProtocol] | None = cls.protocols.get(protocol_name)
        if not protocol_class:
            raise ValueError(f"Unsupported protocol: {protocol_name}")
        cls._instance = protocol_class()
        return cls._instance
