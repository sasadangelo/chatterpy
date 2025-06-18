# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
from providers.llamacpp_provider import LLamaCppProvider
from providers.ollama_provider import OllamaProvider
from providers.openai_provider import OpenAIProvider
from providers.watsonx_provider import WatsonXProvider
from providers.provider import LLMProvider


class LLMProviderFactory:
    # Mapping of provider names to their corresponding classes
    providers = {
        "llamacpp": LLamaCppProvider,
        "ollama": OllamaProvider,
        "openai": OpenAIProvider,
        "watsonx": WatsonXProvider,
    }

    # Singleton instance to ensure only one provider is created at a time
    _instance = None

    @classmethod
    def get_provider(cls, config: dict) -> LLMProvider:
        """
        Returns a singleton instance of an LLM provider based on the config.

        If an instance already exists, it returns that instance to avoid multiple
        instantiations. Otherwise, it creates a new provider instance according
        to the 'provider' specified in the config.

        Args:
            config (dict): Configuration dictionary containing at least a 'provider' key.

        Returns:
            LLMProvider: An instance of a subclass of LLMProvider matching the config.

        Raises:
            ValueError: If the specified provider is not supported.
        """
        # Return existing instance if already created
        if cls._instance is not None:
            return cls._instance

        # Extract provider name from config
        provider_name = config["provider"]
        # Retrieve the provider class from the mapping
        provider_class = cls.providers.get(provider_name)
        # Raise error if provider is unsupported
        if not provider_class:
            raise ValueError(f"[LLMProviderFactory] Unsupported provider: {provider_name}")
        # Create and store the singleton provider instance
        cls._instance = provider_class(config)
        return cls._instance
