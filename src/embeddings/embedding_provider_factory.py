from embeddings.ollama_embedding_provider import OllamaEmbeddingProvider


class EmbeddingProviderFactory:
    providers = {
        "ollama": OllamaEmbeddingProvider,
    }

    # The single provider instance
    _instance = None

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
