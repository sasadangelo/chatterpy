# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from typing import Dict, Type, Optional
from embeddings.embedding_provider import EmbeddingProvider
from embeddings.ollama_embedding_provider import OllamaEmbeddingProvider


class EmbeddingProviderFactory:
    providers: Dict[str, Type[EmbeddingProvider]] = {
        "ollama": OllamaEmbeddingProvider,
        # Add other providers here
    }

    # The single provider instance
    _instance: Optional[EmbeddingProvider] = None

    @classmethod
    def get_embedding_provider(cls, config):
        # If the instance already exists, return it
        if cls._instance is not None:
            return cls._instance

        # Otherwise, create it
        provider_name = config["embedding_provider"]
        provider_class = cls.providers.get(provider_name)
        if not provider_class:
            raise ValueError(f"Unsupported provider: {provider_name}")
        cls._instance = provider_class(config)
        return cls._instance
